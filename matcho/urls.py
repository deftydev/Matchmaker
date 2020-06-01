from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path('position/<slug>', views.position_match_view, name='position_match_view_url'),
    path('employer/<slug>', views.employer_match_view, name='employer_match_view_url'),
    path('location/<slug>', views.location_match_view, name='location_match_view_url'),
]
