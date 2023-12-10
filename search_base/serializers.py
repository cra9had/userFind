from django.utils import timezone
from rest_framework import serializers
from .models import SearchHistory, Person
from .tasks import search_person


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["pk", "search_type", "search_query"]

    def validate_search_query(self, value_dict):
        if type(value_dict) != dict:
            raise serializers.ValidationError("Search query type must be a dict")

        if "phone_number" in value_dict:
            phone_number = value_dict["phone_number"].replace("+", "")
            if type(phone_number) != str:
                raise serializers.ValidationError("phone_number must be a string")
            if phone_number[0] != "7" or len(phone_number) != 11:
                raise serializers.ValidationError("Неверный формат")
            value_dict["phone_number"] = phone_number
        elif "fullname" in value_dict and "birthday" in value_dict:
            pass
        else:
            raise serializers.ValidationError("Neither phone number or fullname with birthday was not provided")

        return value_dict

    def create(self, validated_data):
        user = self.context.get("user")
        try:
            return SearchHistory.objects.get(
                user=user,
                search_type=validated_data["search_type"],
                search_query=validated_data["search_query"],
                date_created__contains=timezone.now().date(),
            )
        except SearchHistory.DoesNotExist:
            pass
        search_history = SearchHistory.objects.create(
            user=user,
            search_type=validated_data["search_type"],
            search_query=validated_data["search_query"],
        )
        search_person.delay(search_history.pk)
        return search_history
