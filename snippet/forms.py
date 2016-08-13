from datetime import timedelta
from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from .models import Snippet, Language


class SnippetForm(forms.ModelForm):
    language = forms.ModelChoiceField(
        label=_("Language"),
        queryset=Language.objects.all(),
        empty_label=_('Auto-detect'),
        required=False
    )

    class Meta:
        model = Snippet
        fields = ['title', 'file_name', 'language', 'content', 'accessibility', 'expiration']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('My cool snippet')}),
            'file_name': forms.TextInput(attrs={'placeholder': _('File name, including extension')}),
            'content': forms.Textarea(attrs={'placeholder': _('Paste code here')}),
            'accessibility': forms.RadioSelect(),
        }

    def __init__(self, user, *args, **kwargs):
        super(SnippetForm, self).__init__(*args, **kwargs)

        if user.is_authenticated():
            self.instance.user = user
        else:
            self.fields['accessibility'].choices = self.fields['accessibility'].choices[0:2]

        self.fields['expiration'].initial = now() + timedelta(minutes=30)

    def clean(self):
        data = self.cleaned_data

        if ("language" not in data \
            or not data["language"] \
            or data["language"].language_code == "autodetect") \
           and "content" in data:
            data["language"] = Language.guess_language(
                filename=data["file_name"],
                text=data["content"],
            )

        return data


ORDER_BY = (
    ('latest', _('Latest')),
    ('oldest', _('Oldest')),
)


class FilterForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=255, required=False)
    users = forms.CharField(label=_('Users'), max_length=255, required=False)
    language = forms.ModelMultipleChoiceField(label=_('Language'), queryset=Language.objects.exclude(slug='autodetect'),
                                              required=False)
    content = forms.CharField(label=_('Code'), max_length=255, required=False, widget=forms.Textarea())
    order_by = forms.ChoiceField(label=_('Ordering'), choices=ORDER_BY, initial=ORDER_BY[0][0], required=False)
    show_code = forms.BooleanField(label=_('Show code'), initial=False, required=False)

    def clean(self):
        data = self.cleaned_data

        if self._filter_by('users'):
            data['users'] = [u.strip() for u in data['users'].split(',')]

        return data

    def advanced_fields(self):
        return [self[field] for field in ['title', 'users', 'language', 'content']]

    def basic_fields(self):
        return [self['order_by'], self['show_code']]

    def apply_filters(self, qs):
        if self._filter_by('title'):
            qs = qs.filter(title__contains=self.cleaned_data['title'])

        if self._filter_by('users'):
            qs = qs.filter(user__in=User.objects.filter(username__in=self.cleaned_data['users']))

        if self._filter_by('language'):
            qs = qs.filter(language__in=self.cleaned_data['language'])

        if self._filter_by('content'):
            qs = qs.filter(content__contains=self.cleaned_data['content'])

        if self._filter_by('order_by'):
            if self.cleaned_data['order_by'] == 'latest':
                qs = qs.order_by('-pub_date', '-id')
            else:
                qs = qs.order_by('id')
        else:
            qs = qs.order_by('-pub_date', '-id')

        return qs

    def _filter_by(self, k):
        return k in self.cleaned_data and len(self.cleaned_data[k])
