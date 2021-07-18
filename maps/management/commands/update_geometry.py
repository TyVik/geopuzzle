import logging

from django.core.management import BaseCommand, CommandError

from maps.forms import UpdateRegionForm
from maps.models import Region

logger = logging.getLogger('commands')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('pk', metavar='pk', type=int, help='Region ID')
        parser.add_argument('--recursive', action='store_true', default=False, help='Recursive')
        parser.add_argument('--with-wiki', action='store_true', default=False, help='Update infobox')

    def handle(self, **options):
        try:
            region = Region.objects.get(pk=options['pk'])
        except ValueError:
            raise CommandError('Please specify the pk')

        params = {
            'recursive': options['recursive'],
            'with_wiki': options['with_wiki'],
            'max_level': 12
        }
        form = UpdateRegionForm(params)
        if form.is_valid():
            form.handle(region)
        else:
            logger.error('UpdateRegionForm is not valid')
