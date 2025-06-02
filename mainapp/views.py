from django.shortcuts import render
from .models import *
from django.db import transaction
from django.core.management import call_command
from rest_framework.decorators import api_view
from mainapp.scraper.scraper_P import scrape_google_paa
from rest_framework.response import Response
from rest_framework import status
import asyncio


# Create your views here.
def index(request):
    return render(request, "home.html")

# @api_view(['POST'])
# def run_scraper_api(request):
#     main_kw = request.data.get("main_kw", "").strip()
#     if not main_kw:
#         return Response({"message": "Main Keyword is required!"}, status=status.HTTP_400_BAD_REQUEST)

#     main_kw_obj = asyncio.run(scrape_google_paa(main_kw))
#     if not main_kw_obj:
#         return Response({"message": "Error running scraper!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     results = GPaaResult.objects.filter(main_kw=main_kw_obj).values()

#     return Response({"main_kw": main_kw_obj.name, "results": list(results)}, status=status.HTTP_200_OK)

def pricing_view(request):
    return render(request, "pricing.html")

def contact_view(request):
    return render(request, "contact.html")