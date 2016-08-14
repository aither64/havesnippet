from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename, get_lexer_for_filename
from pygments.lexers import guess_lexer
import pygments.util
from snippet.utils import gen_string


class Language(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    language_code = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_use_count(self):
        return Snippet.objects.filter(language=self).count()

    def admin_get_use_count(self):
        return "%d&times;" % self.get_use_count()
    admin_get_use_count.short_description = _("Use count")
    admin_get_use_count.allow_tags = True

    @staticmethod
    def guess_language(filename=None, text=None, create=False):
        if filename is None and text is None:
            raise TypeError("guess_language requires either argument filename or text")

        ret = lexer = None

        try:
            if filename and text:
                lexer = guess_lexer_for_filename(filename, text)

            elif filename:
                lexer = get_lexer_for_filename(filename)

            else:
                lexer = guess_lexer(text)

            try:
                ret = Language.objects.filter(language_code__in=lexer.aliases)[0]
            except IndexError:
                if not create:
                    raise pygments.util.ClassNotFound()

                name = lexer.aliases[0]
                ret = Language.objects.create(name=lexer.name, slug=name, language_code=name)

        except pygments.util.ClassNotFound:
            ret = Language.objects.get(language_code="text")

        return ret


ACCESSIBILITY = (
    (0, _('Public')),
    (1, _('Unlisted')),
    (2, _('Logged users')),
    (3, _('Private')),
)


class Snippet(models.Model):
    PUBLIC = 0
    UNLISTED = 1
    LOGGED = 2
    PRIVATE = 3

    title = models.CharField(_('title'), max_length=255, blank=True)
    file_name = models.CharField(_('file name'), max_length=255, blank=True)
    language = models.ForeignKey(Language)
    content = models.TextField(_('code'))
    highlighted_content = models.TextField(_('highlighted code'))
    slug = models.SlugField(max_length=8, unique=True)
    user = models.ForeignKey(User, blank=True, null=True)
    pub_date = models.DateTimeField(_('publish date'), auto_now_add=True)
    update_date = models.DateTimeField(_('updated'), auto_now=True)
    accessibility = models.SmallIntegerField(_('accessibility'), choices=ACCESSIBILITY, default=1)
    expiration = models.DateTimeField(_('expiration'), blank=True, null=True,
                                      help_text=_("leave empty to keep forever"))

    views = models.PositiveIntegerField(_('views'), default=0)
    raw_views = models.PositiveIntegerField(_('raw views'), default=0)
    embed_views = models.PositiveIntegerField(_('embed views'), default=0)
    downloads = models.PositiveIntegerField(_('downloads'), default=0)

    def __str__(self):
        return "{0}: {1}".format(self.slug, self.title)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            self.slug = self.generate_slug()


        lexer = get_lexer_by_name(self.language.language_code)
        formatter = HtmlFormatter(
            linenos=True,
            lineanchors='L',
            anchorlinenos=True,
        )
        self.highlighted_content = highlight(self.content, lexer, formatter)

        if is_new:
            while True:
                try:
                    super(Snippet, self).save(*args, **kwargs)
                    break

                except IntegrityError:
                    self.slug = self.generate_slug()

        else:
            super(Snippet, self).save(*args, **kwargs)

    def accessed(self, type):
        Snippet.objects.filter(pk=self.pk).update(**{type: F(type) + 1})

    def get_title(self):
        return self.title if len(self.title) else _("Untitled")

    def get_absolute_url(self):
        return reverse('snippet_view', kwargs={'code': self.slug})

    @staticmethod
    def generate_slug():
        return gen_string(size=8)
