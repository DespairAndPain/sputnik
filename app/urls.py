
from django.conf.urls import url, include
from django.contrib import admin
import marvel_api.urls

urlpatterns = [
    url(r'^api/', include('marvel_api.urls')),
    url(r'^admin/', admin.site.urls),
]
