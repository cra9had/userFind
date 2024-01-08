from django.db import models
from authentication.models import User


class Transaction(models.Model):
    PAYOK = 0
    OXA_PAY = 1
    TRX_TYPES = (
        (0, "Top up"),
        (1, "Buy")
    )
    TOP_UP_METHODS = (
        (PAYOK, "PayOk"),
        (OXA_PAY, "OxaPay"),
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="User")
    trx_type = models.IntegerField(choices=TRX_TYPES, verbose_name="Transaction type")
    top_up_method = models.IntegerField(choices=TOP_UP_METHODS, verbose_name="Top up method", null=True, blank=True)
    amount = models.IntegerField(verbose_name="Amount", help_text="RUB")
    is_done = models.BooleanField(verbose_name="Is done", default=False)

    def __str__(self):
        prefix = "?" if not self.is_done else ""
        return f"{prefix}Transaction {self.amount} RUB "


class Order(models.Model):
    ORDER_PRODUCTS = (
        (0, "3 searches"),
        (1, "10 searches"),
        (2, "50 searches"),
        (3, "100 searches"),
    )
    date_created = models.DateField(auto_now_add=True, verbose_name="Date")
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT,
                                    verbose_name="Transaction")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="User")
    order_product = models.IntegerField(choices=ORDER_PRODUCTS, verbose_name="Order product")

    def __str__(self):
        return f"Order {self.pk}: {self.get_order_product_display()} User: {self.user}"
