from enum import Enum

from django.db import models


class Status(Enum):
    PROCESSING = ('processing', 'processing')
    FINISHED = ('finished', 'finished')
    CANCELED = ('canceled', 'canceled')

    @classmethod
    def choices(cls):
        return ((status.value[0], status.value[1]) for status in cls)

    @property
    def as_string(self):
        return self.value[0]


class Transaction(models.Model):
    click_trans_id = models.BigIntegerField(default=0)
    merchant_trans_id = models.CharField(max_length=255)
    amount = models.BigIntegerField(default=0)
    action = models.IntegerField(default=0)
    sign_string = models.CharField(max_length=255)
    sign_datetime = models.DateTimeField(max_length=255)
    status = models.CharField(
        max_length=25,
        choices=Status.choices(),
        default=Status.PROCESSING.as_string
    )

    def __str__(self) -> str:
        return str(self.click_trans_id)
