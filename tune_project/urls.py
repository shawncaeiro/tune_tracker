"""tune_project URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin

from tune_throwback import views

urlpatterns = [
    url(r'spotify_auth/(?P<state>\d+)', views.spotify_auth, name='spotify_auth'),
    url(r'spotify_return/$', views.spotify_return, name="spotify_return"),
    url(r'spotify_success/', views.spotify_success, name="spotify_success"),
    url(r'results/(?P<song_id>\d+)/$', views.results_page, name='results_ided'),
    url(r'results/random/', views.results_page_random, name='results'),
    url(r'results', views.results_page, name='results'),
    url(r'^admin/', admin.site.urls),
    url(r'$', views.home_page, name='home'),
]