from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # path('api/run-scraper/', run_scraper_api, name='run_scraper_api'),
    path('pricing', pricing_view, name='pricing'),
    path('contact', contact_view, name='contact'),
]
