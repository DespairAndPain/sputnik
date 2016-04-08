from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from marvel_api import views
import marvel_api.urls


urlpatterns = [
    url(r'^$', views.base),
    url(r'^api/', include('marvel_api.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
