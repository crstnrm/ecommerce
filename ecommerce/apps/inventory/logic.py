from django.core.exceptions import ValidationError
from inventory.models import Movement, Product

from inventory.constants import MovementType
from ecommerce.core.logic import BaseLogic


class ProductLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = Product


class MovementLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = Movement

    def create(
        self, 
        product_id: int, 
        quantity: int, 
        type: int, 
        **kwargs
    ) -> Movement:

        if type == MovementType.INGRESS.value:
            return super().create(
                product_id=product_id, 
                quantity=quantity, 
                type=type, 
                **kwargs
            )

        balance = self.get_balance_by_product_id(product_id=product_id)
        if (balance - quantity) < 0:
            raise ValidationError(
                'Product balance can not be a negative number.'
            )

        return super().create(
            product_id=product_id, 
            quantity=quantity, 
            type=type, 
            **kwargs
        )

    def get_balance_by_product_id(self, product_id: str):
        pass
