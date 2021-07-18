from decimal import Decimal

from django.core.exceptions import ValidationError
from payments.models import Payment, PaymentOrder

from orders.logic import NoteLogic
from ecommerce.core.logic import BaseLogic


class PaymentLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = Payment


class PaymentOrderLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = PaymentOrder

    def create(self, order_id: int, amount: Decimal, **kwargs) -> PaymentOrder:

        note_logic = NoteLogic()
        order_debt = note_logic.get_debt_by_order_id(order_id=order_id)
        if (order_debt - amount) < 0:
            raise ValidationError(
                'There is an overpayment to cover'
                f' the debt of the order id {order_id}'
            )

        return super().create(order_id=order_id, amount=amount, **kwargs)
