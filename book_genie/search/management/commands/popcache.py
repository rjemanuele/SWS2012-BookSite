from django.core.management.base import BaseCommand, CommandError
import book_genie.search.amazon as amazon

class Command(BaseCommand):
    help = 'Fills the cache'

    def handle(self, *args, **options):
        amazon.prepopulate_cache()
