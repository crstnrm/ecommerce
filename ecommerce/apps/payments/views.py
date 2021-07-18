from orders.logic import NoteLogic, OrderLogic
from django.db import transaction
from django.utils import timezone
from payments.logic import PaymentLogic, PaymentOrderLogic
from rest_framework import serializers, status
from rest_framework.response import Response

from ecommerce.core.views import BaseDetailView, BaseView


class PaymentView(BaseView):
    
    class InputSerializer(serializers.Serializer):
        orders_id = serializers.ListField(child=serializers.IntegerField())
        amount = serializers.DecimalField()

    def __init__(self):
        super().__init__()

        self.logic = PaymentLogic()

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        orders_id = serializer.validated_data['orders_id']
        amount = serializer.validated_data['amount']
        
        now = timezone.now()
        payment = self.logic.create(amount=amount, paid_at=now)
        payment_id = payment.id

        payment_order_logic = PaymentOrderLogic()
        note_logic = NoteLogic()

        for order_id in orders_id:
            
            total_debt = note_logic.get_debt_by_order_id(order_id=order_id)
            partial_amount = min(amount, total_debt)
            
            payment_order_logic.create(
                payment_id=payment_id, 
                order_id=order_id,
                amount=partial_amount
            )
            note_logic.update_outstanding_amount_by_order_id(
                order_id=order_id, amount=partial_amount
            )
            
            amount -= partial_amount

        data = self.logic.serialize(payment)
        return Response(data, status=status.HTTP_201_CREATED)
        

class PaymentDetailView(BaseDetailView):
    
    def __init__(self):
        super().__init__()

        self.logic = PaymentLogic()
