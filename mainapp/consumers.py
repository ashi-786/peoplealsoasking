import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mainapp.scraper.scraper_P import scrape_google_paa
from .models import *
from asgiref.sync import sync_to_async

class ScraperConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "WebSocket connected"}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "run_scraper":
            main_kw = data.get("main_kw").strip()
            if not main_kw:
                await self.send(json.dumps({"type": "scraper_error", "message": "Main keyword is required!"}))
                return
            
            try:
                await self.send(json.dumps({"message": f"Running scraper for '{main_kw}'..."}))
                main_kw_obj = await scrape_google_paa(main_kw)
                print(main_kw_obj)
                if not main_kw_obj:
                    await self.send(json.dumps({"type": "scraper_error", "message": "Error running scraper!"}))
                results = await sync_to_async(GPaaResult.objects.filter(main_kw=main_kw_obj).values)()
                print(type(results))
                await self.send(json.dumps({
                    "type": "scraper_result",
                    "main_kw": main_kw_obj.name,
                    "results": results
                }))
            except Exception as e:
               await self.send(json.dumps({"type": "scraper_error", "message": str(e)}))