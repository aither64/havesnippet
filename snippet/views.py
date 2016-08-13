from django.conf import settings
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
from snippet.forms import SnippetForm, FilterForm, BookmarkForm
from snippet.models import Snippet, Bookmark
from snippet.utils import return_url


def paste(request):
    if not settings.SNIPPET_PASTE_PUBLIC:
        raise PermissionDenied

    if request.method == "POST":
        form = SnippetForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect('snippet-view', code=form.instance.slug)

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
            return redirect('snippet-view', code=form.instance.slug)

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

    return redirect('snippet.views.profile')


class SnippetView(View):
    def get(self, request, code):
        snippet = get_object_or_404(Snippet, slug=code)

        if (snippet.accessibility == Snippet.LOGGED and not request.user.is_authenticated()) \
                or snippet.accessibility == Snippet.PRIVATE and snippet.user != request.user:
            raise PermissionDenied

        return self.view(request, snippet)

    def view(self, request, snippet):
        context = {
            'snippet': snippet,
        }

        if request.user.is_authenticated():
            context['user_bookmarks'] = [b.snippet for b in Bookmark.objects.filter(owner=request.user).exclude(snippet=None)]

        return render(request, 'snippet/view.html', context)


class DownloadSnippetView(SnippetView):
    def view(self, request, snippet):
        res = HttpResponse(snippet.content, content_type='text/plain')
        res['Content-Disposition'] = 'attachment; filename={0}.txt'.format(snippet.slug)
        return res


class RawSnippetView(SnippetView):
    def view(self, request, snippet):
        return HttpResponse(snippet.content, content_type='text/plain')


@login_required
def profile(request):
    return render(request, 'snippet/profile.html', {
        'api_keys': AuthKey.objects.filter(user=request.user),
        'key_form': AuthKeyAddForm(),
    })


def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, "snippet/user.html", {
        'profile_user': user,
        'public_snippet_cnt': Snippet.objects.filter(user=user, accessibility=Snippet.PUBLIC).count(),
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

        if context['show_code'] and request.user.is_authenticated():
            context['user_bookmarks'] = [b.snippet for b in Bookmark.objects.filter(owner=request.user).exclude(snippet=None)]

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


#class BookmarksBrowseView(BrowseView):
#    logged = True
#    template_page = "snippet/my_snippets_page.html"
#
#    def access_cond(self):
#        return Q(user=self.request.user)
#
#    def queryset(self):
#        Bookmark.objects.filter(owner=self.request.user).exclude(snippet=None)
#        return super(BookmarksBrowseView, self).queryset().filter()


@login_required
def bookmarks(request):
    return render(request, "snippet/bookmarks.html", {
        'bookmarks_snippets': Bookmark.objects.filter(owner=request.user).exclude(snippet=None),
    })


@login_required
def bookmark_snippet(request, code):
    snippet = get_object_or_404(Snippet, slug=code)
    template = "snippet/bookmark_page.html" if request.is_ajax() else "snippet/bookmark.html"

    if request.method == "POST":
        form = BookmarkForm(request.POST)

        if form.is_valid():
            form.instance.snippet = snippet
            form.instance.owner = request.user

            try:
                form.save()
            except IntegrityError:
                if request.is_ajax():
                    return HttpResponse("ERROR")

                messages.error(request, _("Bookmark already exists."))
            else:
                if request.is_ajax():
                    return HttpResponse("OK")

                messages.success(request, _("Bookmark saved."))

            return redirect(form.cleaned_data['next'])

    else:
        form = BookmarkForm(initial={'next': return_url(request, snippet.get_absolute_url())})

    return render(request, template, {
        'snippet': snippet,
        'form': form
    })


@login_required
def bookmark_snippet_delete(request, code):
    bookmark = get_object_or_404(Bookmark, owner=request.user, snippet=get_object_or_404(Snippet, slug=code))
    bookmark.delete()

    messages.success(request, _("Bookmark deleted."))

    return redirect(return_url(request, reverse('snippet-browse-bookmarks')))
