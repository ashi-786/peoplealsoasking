import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mainapp.scraper.scraper_P import scrape_google_paa
from .models import *
from asgiref.sync import sync_to_async

class ScraperConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'scraper'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(json.dumps({"message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "run_scraper":
            main_kw = data.get("main_kw").strip()
            if not main_kw:
                await self.send(json.dumps({"type": "scraper_error", "message": "Main keyword is required!"}))
                return
            
            await self.send(json.dumps({"message": f"Running scraper for '{main_kw}'..."}))

            try:
                main_kw_obj = await scrape_google_paa(main_kw)
                if not main_kw_obj:
                    await self.send(json.dumps({"type": "scraper_error", "message": "Error running scraper!"}))
                results = await sync_to_async(GPaaResult.objects.filter(main_kw=main_kw_obj).values)()
                await self.send(json.dumps({
                    "type": "scraper_result",
                    "main_kw": main_kw_obj.name,
                    "results": results
                }))
            except Exception as e:
               await self.send(json.dumps({"type": "scraper_error", "message": str(e)}))