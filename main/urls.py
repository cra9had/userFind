from django.urls import path

from .views import home, my, BuyFullDataAPIView, betatransfer


urlpatterns = [
    path("", home, name="home"),
    path("my/", my),
    path("api/buy-full-data/", BuyFullDataAPIView.as_view()),
    path("betatransfer.txt/", betatransfer)
]
