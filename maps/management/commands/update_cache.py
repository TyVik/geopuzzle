import sys

from django.core.cache import cache
from django.core.management.base import LabelCommand, CommandError, BaseCommand

from maps.models import Region


class Command(LabelCommand):

    def print_help(self, prog_name, subcommand):
        super(Command, self).print_help(prog_name, subcommand)

    def handle(self, *labels, **options):
        if not labels:
            print(self.print_help('update_cache', ''))
            sys.exit(1)

        for label in labels:
            if label not in Region.caches.keys():
                raise CommandError('`%s` unknown cache' % label)
            for region in Region.objects.all().iterator():
                cache.delete(region.caches[label].format(id=region.id))
                print('===========================')
                print(region.title)
                print(getattr(region, label))
