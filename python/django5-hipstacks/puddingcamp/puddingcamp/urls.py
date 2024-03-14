from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import urlpatterns as staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns.extend(staticfiles_urlpatterns)

