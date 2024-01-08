from django.urls import path

from .views import (BuyFullDataAPIView, OxaPayPaymentAPIView,
                    PayOkPaymentAPIView, BuySearchesAPIView, GetBonusAPIView)


urlpatterns = [
    path("api/oxapay/payment/", OxaPayPaymentAPIView.as_view()),
    path("api/payok/payment/", PayOkPaymentAPIView.as_view()),
    path("api/buy-full-data/", BuyFullDataAPIView.as_view()),
    path("api/buy-searches/", BuySearchesAPIView.as_view()),
    path("api/get-bonus/dOSd4mSMrQ7Djua6<int:telegram_id>6UaMNQp6b5Wxp73Mn", GetBonusAPIView().as_view())
]
