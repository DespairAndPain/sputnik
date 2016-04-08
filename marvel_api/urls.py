from django.conf.urls import patterns,  url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_view
from . import views

urlpatterns = patterns('',
                       url(r'^api-token-auth/', auth_view.obtain_auth_token),
                       url(r'^list$', views.comics_list),
                       url(r'^heroevents$', views.hero_events_list),
                       url(r'^refreshdata$', views.refresh_data),
                       url(r'^similarcomics$', views.similar_comics_data),
                       )

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])