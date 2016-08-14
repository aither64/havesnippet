from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from api.forms import AuthKeyAddForm
from api.models import AuthKey
from snippet.forms import SnippetForm, FilterForm
from snippet.models import Snippet
from snippet.utils import return_url
from snippet import settings


def paste(request):
    if not settings.SNIPPET_PASTE_PUBLIC and not request.user.is_authenticated():
        return redirect('snippet_browse')

    if request.method == "POST":
        form = SnippetForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect('snippet_view', code=form.instance.slug)

    else:
        form = SnippetForm(request.user)

    return render(request, 'snippet/paste.html', {'form': form})


@login_required
def edit(request, code):
    snippet = get_object_or_404(Snippet, slug=code)

    if snippet.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = SnippetForm(request.user, request.POST, instance=snippet)

        if form.is_valid():
            form.save()
            return redirect('snippet_view', code=form.instance.slug)

    else:
        form = SnippetForm(request.user, instance=snippet)

    return render(request, 'snippet/edit.html', {'form': form, 'snippet': snippet})


@login_required
def delete(request, code):
    snippet = get_object_or_404(Snippet, slug=code)

    if snippet.user != request.user:
        raise PermissionDenied

    return render(request, "snippet/delete.html", {'snippet': snippet})


@login_required
def delete_confirm(request, code):
    snippet = get_object_or_404(Snippet, slug=code)

    if snippet.user != request.user:
        raise PermissionDenied

    snippet.delete()

    return redirect('snippet_browse_mine')


class SnippetView(View):
    def get(self, request, code):
        snippet = get_object_or_404(Snippet, slug=code)

        if (snippet.accessibility == Snippet.LOGGED and not request.user.is_authenticated()) \
                or snippet.accessibility == Snippet.PRIVATE and snippet.user != request.user:
            raise PermissionDenied

        return self.view(request, snippet)

    def view(self, request, snippet):
        snippet.accessed('views')

        context = {
            'snippet': snippet,
        }

        return render(request, 'snippet/view.html', context)


class DownloadSnippetView(SnippetView):
    def view(self, request, snippet):
        snippet.accessed('downloads')

        res = HttpResponse(snippet.content, content_type='text/plain')
        res['Content-Disposition'] = 'attachment; filename={0}'.format(
            snippet.file_name or (snippet.slug + '.txt')
        )
        return res


class RawSnippetView(SnippetView):
    def view(self, request, snippet):
        snippet.accessed('raw_views')

        return HttpResponse(snippet.content, content_type='text/plain')


class EmbedSnippetView(SnippetView):
    def view(self, request, snippet):
        snippet.accessed('embed_views')

        return render(request, 'snippet/embed.html', {'snippet': snippet})


class MaxSnippetView(SnippetView):
    def view(self, request, snippet):
        snippet.accessed('views')

        return render(request, 'snippet/view.html', {
            'snippet': snippet,
            'snippet_max': True,
        })


@login_required
def profile(request):
    return render(request, 'snippet/profile.html', {
        'api_keys': AuthKey.objects.filter(user=request.user),
        'key_form': AuthKeyAddForm(),
    })


class BrowseView(View):
    http_method_names = ['get']
    template = "snippet/browse.html"
    template_page = "snippet/browse_page.html"
    form_class = FilterForm
    logged = False

    def get(self, request):
        if self.logged and not request.user.is_authenticated():
            raise PermissionDenied

        self.request = request
        self.form = self.form_class(request.GET)

        if not self.form.is_valid():
            return render(request, self.template, {'form': self.form})

        snippets = self.queryset()
        context = {
            'snippets': snippets,
            'form': self.form,
            'self_url': request.META['PATH_INFO'],
            'show_code': self.form.cleaned_data['show_code'],
            'template_page': self.template_page,
        }

        context.update(self.context())

        return render(request, self.template_page if request.is_ajax() else self.template, context)

    def access_cond(self):
        cond = Q(accessibility=Snippet.PUBLIC)

        if self.request.user.is_authenticated():
            cond |= Q(accessibility=Snippet.LOGGED)

        return cond

    def queryset(self):
        return self.form.apply_filters(Snippet.objects.filter(self.access_cond()))

    def context(self):
        return {}


class MySnippetsView(BrowseView):
    logged = True

    def access_cond(self):
        return Q(user=self.request.user)
