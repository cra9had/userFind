from django.urls import path

from .views import top_up, home, my, BuyFullDataAPIView, payok


urlpatterns = [
    path("", home, name="home"),
    path("payok_project_verification.txt", payok),
    path("my/", my),
    path("topup/", top_up, name="topup"),
    path("api/buy-full-data/", BuyFullDataAPIView.as_view())
]
