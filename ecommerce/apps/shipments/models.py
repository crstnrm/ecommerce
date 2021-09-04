from django.db import models
from shipments.constants import ShipmentProductStatus, ShipmentStatus
from ecommerce.core.models import BaseModel


class Shipment(BaseModel):
    order = models.ForeignKey(
        'orders.Order',
        related_name='shipments',
        on_delete=models.PROTECT
    )
    provider = models.ForeignKey(
        'Provider',
        related_name='shipments',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    status = models.IntegerField(default=ShipmentStatus.CREATED.value)


class ShipmentProduct(BaseModel):
    shipment = models.ForeignKey(
        'Shipment',
        related_name='products',
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        'inventory.Product',
        related_name='shipments',
        on_delete=models.PROTECT
    )
    status = models.IntegerField(default=ShipmentStatus.CREATED)


class Provider(BaseModel):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
