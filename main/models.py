from django.db import models
from authentication.models import User


class Transaction(models.Model):
    TRX_TYPES = (
        (0, "Top up"),
        (1, "Buy")
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="User")
    trx_type = models.IntegerField(choices=TRX_TYPES, verbose_name="Transaction type")
    amount = models.IntegerField(verbose_name="Amount", help_text="RUB")
    is_done = models.BooleanField(verbose_name="Is done", default=False)

    def save(self, *args, **kwargs):
        if self.pk:     # Model updated
            return super(Transaction, self).save(*args, **kwargs)
        if self.trx_type == 1 and self.is_done:
            assert self.user.balance >= self.amount
            self.user.balance -= self.amount
        self.user.save()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        prefix = "?" if not self.is_done else ""
        return f"{prefix}Transaction {self.amount} RUB "


class Order(models.Model):
    ORDER_PRODUCTS = (
        (0, "Full data"),
    )
    date_created = models.DateField(auto_now_add=True, verbose_name="Date")
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT,
                                    verbose_name="Transaction")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="User")
    order_product = models.IntegerField(choices=ORDER_PRODUCTS, verbose_name="Order product")

    def __str__(self):
        return f"Order {self.pk}: {self.get_order_product_display()} User: {self.user}"
