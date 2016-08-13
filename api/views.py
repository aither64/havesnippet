import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from taggit.models import Tag
from api.forms import SnippetForm, ApiForm, AuthKeyAddForm, LanguageDetectForm
from api.models import AuthKey
from snippet.models import Language, Snippet


def about(request):
    return render(request, "api/about.html", {
        'langs': [l.language_code for l in Language.objects.all()],
    })


@login_required
@require_POST
def key_add(request):
    form = AuthKeyAddForm(request.user, request.POST)

    if form.is_valid():
        form.save()
        return redirect('snippet.views.profile')

    return render(request, 'snippet/profile.html', {
        'api_keys': AuthKey.objects.filter(user=request.user),
        'key_form': form
    })


@login_required
def key_delete(request, key):
    get_object_or_404(AuthKey, user=request.user, key=key).delete()

    return redirect('snippet.views.profile')


class BaseView(View):
    http_method_names = ['get']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.validate_user(request)

        self.request = request
        self.args = args
        self.kwargs = kwargs

        return super(BaseView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.process(request.GET)

    def post(self, request):
        return self.process(request.POST)

    def validate_user(self, request):
        self.user = None
        form = ApiForm(request.POST if request.method == "POST" else request.GET)

        if not form.is_valid():
            raise PermissionDenied

        if form.auth_key:
            form.accept()
            self.user = form.auth_key.user

    def process(self, params):
        self.prepare(params)

        if "format" in params:
            if params["format"] == "json":
                return self.json()

        return self.plain()

    def prepare(self, params):
        pass

    def json(self):
        raise NotImplemented

    def plain(self):
        raise NotImplemented


class PasteView(BaseView):
    http_method_names = ['post']

    def __init__(self, *args, **kwargs):
        super(PasteView, self).__init__(*args, **kwargs)

        self.paste = (None, None)

    def prepare(self, params):
        form = SnippetForm(params)

        if form.is_valid():
            form.instance.user = self.user
            form.save()
            self.paste = (True, self.request.build_absolute_uri(form.instance.get_absolute_url()))

        else:
            self.paste = (False, form.errors)

    def json(self):
        ret = {}

        if self.paste[0]:
            ret['url'] = self.paste[1]
        else:
            ret['error'] = self.paste[1]

        return HttpResponse(json.dumps(ret))

    def plain(self):
        if self.paste[0]:
            return HttpResponse(self.paste[1])

        return HttpResponse("ERROR:" + ",".join(self.paste[1]))


class LanguagesView(BaseView):
    def prepare(self, params):
        self.qs = Language.objects.all().order_by('slug')

    def json(self):
        ret = {}

        for lang in self.qs:
            ret[lang.language_code] = lang.name

        return HttpResponse(json.dumps(ret))

    def plain(self):
        res = HttpResponse()

        for lang in self.qs:
            res.write("{0}={1}\n".format(lang.language_code, lang.name))

        return res


class TagsView(BaseView):
    def prepare(self, params):
        self.qs = Tag.objects.all()

    def json(self):
        ret = []

        for tag in self.qs:
            ret.append(tag.name)

        return HttpResponse(json.dumps(ret))

    def plain(self):
        res = HttpResponse()

        for tag in self.qs:
            res.write("{0}\n".format(tag.name))

        return res


class ViewView(BaseView):
    def prepare(self, params):
        self.snippet = get_object_or_404(Snippet, slug=self.kwargs['code'])

    def json(self):
        return HttpResponse(json.dumps({
            'title': self.snippet.title,
            'language': self.snippet.language.language_code,
            'code': self.snippet.content,
            'author': self.snippet.get_author(),
            'date': self.snippet.date,
            'tags': [t.name for t in self.snippet.tags.all()],
        }))

    def plain(self):
        return HttpResponse(self.snippet.content)


class DetectLanguageView(BaseView):
    http_method_names = ['post']

    def prepare(self, params):
        form = LanguageDetectForm(params)

        if form.is_valid():
            lang = Language.guess_language(create=False, **form.cleaned_data)
            self.ret = {'language': lang.language_code}

        else:
            self.ret = {'error': form.errors}

    def json(self):
        s = json.dumps(self.ret)

        if 'error' in self.ret:
            return HttpResponseBadRequest(s)
        else:
            return HttpResponse(s)

    def plain(self):
        if 'error' in self.ret:
            return HttpResponseBadRequest("ERROR:" + ",".join(self.ret['errors']))
        else:
            return HttpResponse(self.ret['language'])
