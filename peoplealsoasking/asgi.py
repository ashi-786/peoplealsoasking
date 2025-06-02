# import sys
# import asyncio

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# print(f"Event loop policy: {asyncio.get_event_loop_policy()}")

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peoplealsoasking.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from mainapp.consumers import *


ws_pattern= [
    re_path(r"ws/api/run-scraper/$", ScraperConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(ws_pattern)
        )
    ),
})