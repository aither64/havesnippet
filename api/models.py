from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from snippet.utils import gen_string


class AuthKey(models.Model):
    user = models.ForeignKey(User)
    key = models.SlugField(max_length=40, unique=True)
    description = models.CharField(_('description'), max_length=100)
    use_count = models.IntegerField(_('use count'), default=0)
    last_use = models.DateTimeField(_('last use'), blank=True, null=True)

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.key = self.generate_key()

            while True:
                try:
                    super(AuthKey, self).save(*args, **kwargs)
                    break
                except IntegrityError:
                    self.key = self.generate_key()

        else:
            super(AuthKey, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return gen_string(size=40)
