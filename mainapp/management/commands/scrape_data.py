# mainapp/management/commands/scrape_data.py
import asyncio
from django.core.management.base import BaseCommand
from mainapp.scraper.scraper_P import scrape_google_paa

class Command(BaseCommand):
    help = "Run Scraper"

    def add_arguments(self, parser):
        parser.add_argument("main_kw", type=str)

    def handle(self, *args, **kwargs):
        main_kw = kwargs["main_kw"]
        try:
            main_kw_obj = asyncio.run(scrape_google_paa(main_kw))
            self.stdout.write(self.style.SUCCESS(f"Scraped and saved results for '{main_kw_obj.name}'"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error scraping '{main_kw}': {str(e)}"))
