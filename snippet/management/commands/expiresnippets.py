from django.core.management import BaseCommand, CommandError
from django.utils import timezone
from snippet.models import Snippet


class Command(BaseCommand):
    help = 'Delete expired snippets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quiet',
            action='store_true',
            dest='quiet',
            default=False,
            help='Suppress any output except errors',
        )

    def handle(self, *args, **options):
        qs = Snippet.objects.filter(
            expiration__lt=timezone.now()
        ).order_by('pub_date', 'update_date')

        if not options['quiet']:
            for s in qs:
                print('{0} {1}'.format(s.slug, s.expiration))

        n, _ = qs.delete()

        if not options['quiet']:
            print("Deleted {0} snippets".format(n))
