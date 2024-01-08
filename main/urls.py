from django.urls import path

from .views import (BuyFullDataAPIView, OxaPayPaymentAPIView,
                    PayOkPaymentAPIView, BuySearchesAPIView)


urlpatterns = [
    path("api/oxapay/payment/", OxaPayPaymentAPIView.as_view()),
    path("api/payok/payment/", PayOkPaymentAPIView.as_view()),
    path("api/buy-full-data/", BuyFullDataAPIView.as_view()),
    path("api/buy-searches/", BuySearchesAPIView.as_view()),
]
