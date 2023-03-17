
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name="home page"),
    path("api/",include("api.urls")),
]

urlpatterns += staticfiles_urlpatterns()

