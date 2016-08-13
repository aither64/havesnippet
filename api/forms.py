from datetime import datetime
from django import forms
from django.conf import settings
from django.db.models import F
from django.utils.timezone import now, utc
from api.models import AuthKey
from snippet.models import Snippet, Language


class AuthKeyAddForm(forms.ModelForm):
    class Meta:
        model = AuthKey
        fields = ['description']

    def __init__(self, user=None, *args, **kwargs):
        super(AuthKeyAddForm, self).__init__(*args, **kwargs)

        self.user = user

    def clean(self):
        self.instance.user = self.user

        return self.cleaned_data


class ApiForm(forms.Form):
    api_key = forms.CharField(max_length=40, required=not settings.SNIPPET_PASTE_PUBLIC)

    def clean(self):
        data = self.cleaned_data
        self.auth_key = None

        if "api_key" in data and len(data["api_key"]):
            try:
                self.auth_key = AuthKey.objects.get(key=data["api_key"])
            except AuthKey.DoesNotExist:
                raise forms.ValidationError("API key is not valid")

        return data

    def accept(self):
        AuthKey.objects.filter(pk=self.auth_key.pk).update(last_use=now(), use_count=F('use_count') + 1)


class SnippetForm(forms.ModelForm):
    language = forms.CharField(max_length=50)
    expiration = forms.IntegerField(min_value=0)

    class Meta:
        model = Snippet
        fields = ['title', 'file_name', 'language', 'content', 'accessibility', 'expiration']

    def clean_language(self):
        lang = self.cleaned_data["language"]

        try:
            lang = Language.objects.get(slug=lang)
        except Language.DoesNotExist:
            raise forms.ValidationError("language does not exists")

        return lang

    def clean_expiration(self):
        expire = self.cleaned_data["expiration"]

        return datetime.fromtimestamp(expire, utc)


class LanguageDetectForm(forms.Form):
    filename = forms.CharField(max_length=1000, required=False)
    text = forms.CharField(max_length=65535, required=False)

    def clean(self):
        data = self.cleaned_data

        if len(data) == 0:
            raise forms.ValidationError("specify filename, text, or both to be identified")

        return data
