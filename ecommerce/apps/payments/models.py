from payments.constants import PaymentStatus
from ecommerce.core.models import BaseModel
from django.db import models
from django.utils import timezone


class Payment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=PaymentStatus.PENDING.value)


class PaymentOrder(BaseModel):
    payment = models.ForeignKey('Payment', on_delete=models.PROTECT)
    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
