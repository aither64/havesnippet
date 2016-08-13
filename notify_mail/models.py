from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from snippet.models import Snippet, Bookmark


@receiver(post_save, sender=Snippet)
def notify(sender, instance, created, **kwargs):
    qs_args = []
    qs_kwargs = {
        'follow': True
    }

    if created and instance.user:  # inform bookmarks on snippet's owner
        qs_kwargs['user'] = instance.user

    else:
        qs_args.append(Q(user=instance.user) | Q(snippet=instance))

    for bookmark in Bookmark.objects.filter(*qs_args, **qs_kwargs):
        url = 'http://%s%s' % (Site.objects.get_current().domain, bookmark.snippet.get_absolute_url())

        send_mail('Snippet update', url, 'snippet@havefun.cz', [bookmark.user.email],
                  fail_silently=True)
