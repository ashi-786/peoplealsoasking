# mainapp/management/commands/scrape_data.py
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from django.core.management.base import BaseCommand
from mainapp.scraper.scraper_S import scrape_google_paa

class Command(BaseCommand):
    help = "Run Scraper"

    # def add_arguments(self, parser):
    #     parser.add_argument("main_kw", type=str)

    def handle(self, *args, **kwargs):
        # main_kw = kwargs["main_kw"]
        try:
            main_kw_obj = scrape_google_paa("affordable web hosting")
            self.stdout.write(self.style.SUCCESS(f"Scraped and saved results for '{main_kw_obj.name}'"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error scraping: {str(e)}"))

    # def handle(self, *args, **kwargs):
    #     try:
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)
    #         main_kw_obj = loop.run_until_complete(scrape_google_paa("affordable web hosting"))
    #         self.stdout.write(self.style.SUCCESS(f"Scraped and saved results for '{main_kw_obj.name}'"))
    #     except Exception as e:
    #         self.stderr.write(self.style.ERROR(f"Error scraping: {str(e)}"))
    #     finally:
    #         loop.close()
