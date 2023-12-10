from authentication.models import User
from django.db import models


class Person(models.Model):
    phone_number = models.CharField(max_length=20, verbose_name="Phone number", unique=True)
    fullname = models.CharField(max_length=256, verbose_name="Fullname", null=True, blank=True)
    birthday = models.DateField(verbose_name="Birthday", null=True, blank=True)
    email = models.CharField(max_length=256, verbose_name="Email", null=True, blank=True)
    inn = models.CharField(max_length=256, verbose_name="INN", null=True, blank=True)
    driver_license = models.CharField(max_length=64, verbose_name="Driver licence", null=True, blank=True)
    possibles_addresses = models.CharField(max_length=512, verbose_name="Possible addresses", null=True, blank=True)
    passport = models.CharField(max_length=256, verbose_name="Passport", null=True, blank=True)
    insurance = models.CharField(max_length=64, verbose_name="insurance", null=True, blank=True)
    telegram_username = models.CharField(max_length=64, verbose_name="Telegram username", null=True, blank=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return f"{self.fullname} | {self.birthday} | {self.phone_number}"


class SearchHistory(models.Model):
    SEARCH_TYPES = (
        (0, "Phone"),
        (1, "Fullname + birthday")
    )
    SEARCH_STATUSES = (
        (0, "In progress"),
        (1, "Not found"),
        (2, "Success"),
    )
    date_created = models.DateTimeField(auto_now=True, verbose_name="Search date")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    search_type = models.IntegerField(choices=SEARCH_TYPES, verbose_name="Search type")
    search_query = models.JSONField(verbose_name="Search query")
    status = models.IntegerField(choices=SEARCH_STATUSES, verbose_name="Status", default=0)
    search_result_pk = models.IntegerField(verbose_name="Search Person pk", null=True, blank=True)

    class Meta:
        verbose_name = "Search history"
        verbose_name_plural = "Search histories"

    def __str__(self):
        return f"Search №{self.pk}. {self.user} | {self.get_status_display()}"
