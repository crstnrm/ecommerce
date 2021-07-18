from decimal import Decimal
from orders.constants import OrderStatus
from django.core.exceptions import ValidationError

from django.db import transaction
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from orders.models import Order, OrderProduct, Note

from inventory.constants import MovementType
from inventory.logic import MovementLogic
from ecommerce.core.logic import BaseLogic


class OrderLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = Order

    def send_order(self, order_id: int, num_of_products_shipped: int) -> Order:

        order = self.get(id=order_id)
        total_of_products = order.products.count()
        new_order_status = OrderStatus.PARTIAL_SHIPMENT.value
        if total_of_products == num_of_products_shipped:
            new_order_status = OrderStatus.SENT.value

        return self.update(instance=order, status=new_order_status)

    def confirm_order(self, order_id: int) -> None:

        order = self.get(id=order_id)
        self.update(instance=order, status=OrderStatus.PROCESSED.value)


class OrderProductLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = OrderProduct

    @transaction.atomic
    def create(
        self, 
        product_id: int, 
        quantity: int, 
        order_id: int, 
        **kwargs
    ) -> Order:

        order_logic = OrderLogic()
        order = order_logic.get(id=order_id)
        if not order.is_created:
            raise ValidationError(
                f'The order {order_id} is already in process.'
            )

        movement_logic = MovementLogic()
        movement_logic.create(
            product_id=product_id, 
            quantity=quantity, 
            type=MovementType.COMMITTED.value
        )
        return super().create(
            order_id=order_id,
            product_id=product_id, 
            quantity=quantity, 
            **kwargs
        )
    
    def get_total_price_by_order_id(self, order_id: int) -> Decimal:
        
        order_logic = OrderLogic()
        order_exists = order_logic.find(id=order_id).exists()
        if not order_exists():
            raise ValidationError(f'Order {order_id} does not exists.')

        total = self.find(
            order_id=order_id
        ).aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )
        return total['total']


class NoteLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = Note

    @transaction.atomic
    def update_outstanding_amount_by_order_id(
        self, order_id: int, amount: Decimal
    ) -> None:

        order_logic = OrderLogic()
        order = order_logic.get(id=order_id)
        note = order.note
        outstanding = note.outstanding_amount - amount
        if outstanding < 0:
            raise ValueError(f'the amount {amount} is not valid.')

        new_order_status = OrderStatus.PAID.value \
            if outstanding == 0 else OrderStatus.PARTIAL_PAYMENT.value
        order_logic.update(instance=order, status=new_order_status)

        self.update(instance=note, outstanding_amount=outstanding)

    def get_debt_by_order_id(self, order_id: int) -> Decimal:
        
        order_logic = OrderLogic()
        order_exists = order_logic.find(id=order_id).exists()
        if not order_exists():
            raise ValidationError(f'Order {order_id} does not exists.')

        outstanding_amount = self.find(
            order_id=order_id
        ).values_list(
            'outstanding_amount', flat=True
        ).first()

        return outstanding_amount
