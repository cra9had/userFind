from rest_framework import serializers
from .models import Transaction


OXA_PAY_MIN_TOP_UP_AMOUNT_RUB = 10


class TopUpSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
    )
    top_up_method = serializers.IntegerField()

    def validate_amount(self, value):
        if self.initial_data.get("top_up_method") == Transaction.OXA_PAY and value < OXA_PAY_MIN_TOP_UP_AMOUNT_RUB:
            raise serializers.ValidationError(f"Мин. сумма {OXA_PAY_MIN_TOP_UP_AMOUNT_RUB}р")

    def validate_top_up_method(self, value):
        if not value in dict(Transaction.TOP_UP_METHODS):
            raise serializers.ValidationError("Top up method does not exist")
        return value

    def create(self, validated_data):
        trx = Transaction.objects.create(
            user=self.context.get("user"),
            trx_type=0,
            top_up_method=validated_data.get("top_up_method"),
            amount=validated_data.get("amount"),
            is_done=False
        )
        return trx
