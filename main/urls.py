from django.urls import path

from .views import home, my, BuyFullDataAPIView, payok


urlpatterns = [
    path("", home, name="home"),
    path("payok_project_verification.txt", payok),
    path("my/", my),
    path("api/buy-full-data/", BuyFullDataAPIView.as_view())
]
