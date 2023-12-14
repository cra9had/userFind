from django.contrib import admin
from .models import Person, SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_filter = ("status", "search_type", "paid", )
    list_display = ["user", "search_type", "search_query", "status", "search_result_pk", "paid", "date_created"]
    readonly_fields = ("date_created",)


admin.site.register(Person)

