from django.db import models
from ecommerce.core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=150)
    reference = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Movement(BaseModel):
    product = models.ForeignKey(
        'Product', 
        related_name='movements', 
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    type = models.IntegerField()
