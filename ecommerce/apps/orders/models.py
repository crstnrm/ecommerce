from decimal import Decimal
from orders.constants import OrderStatus

from django.conf import settings
from django.db import models

from ecommerce.core.models import BaseModel


class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='orders',
        on_delete=models.PROTECT
    )
    status = models.IntegerField(default=OrderStatus.CREATED.value)

    @property
    def is_created(self) -> bool:
        return self.status == OrderStatus.CREATED.value

    @property
    def is_paid(self) -> bool:
        return self.status == OrderStatus.PAID.value
    
    @property
    def is_partial_shipment(self) -> bool:
        return self.status == OrderStatus.PARTIAL_SHIPMENT.value   


class OrderProduct(BaseModel):
    order = models.ForeignKey(
        'Order', 
        related_name='products', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'inventory.Product',
        related_name='orders',
        on_delete=models.PROTECT
    )
    quantity = models.IntegerField()


class Note(BaseModel):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2)
