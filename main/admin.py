from django.contrib import admin
from .models import Transaction, Order


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ("is_done",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("order_product",)
