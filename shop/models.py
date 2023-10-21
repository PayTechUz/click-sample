from django.db import models


class Order(models.Model):
    order_id = models.CharField(max_length=255)
    amount = models.BigIntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.order_id
