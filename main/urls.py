from django.urls import path

from .views import home, my


urlpatterns = [
    path("", home, name="home"),
    path("my/", my)
]
