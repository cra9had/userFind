from django.urls import path

from .views import home, my, BuyFullDataAPIView, TopUpAPIView, OxaPayPaymentAPIView


urlpatterns = [
    path("", home, name="home"),
    path("my/", my),
    path("api/top-up/", TopUpAPIView.as_view()),
    path("api/oxapay/payment/", OxaPayPaymentAPIView.as_view()),
    path("api/buy-full-data/", BuyFullDataAPIView.as_view()),
]
