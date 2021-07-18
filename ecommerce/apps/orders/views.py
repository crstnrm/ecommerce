from rest_framework import status
from rest_framework.response import Response

from orders.logic import NoteLogic, OrderLogic, OrderProductLogic
from ecommerce.core.views import BaseDetailView, BaseView


class OrderView(BaseView):
    
    def __init__(self):
        super().__init__()

        self.logic = OrderLogic()


class OrderDetailView(BaseDetailView):
    
    def __init__(self):
        super().__init__()

        self.logic = OrderLogic()


class OrderProductView(BaseView):
    
    def __init__(self):
        super().__init__()

        self.logic = OrderProductLogic()

    def post(self, request, *args, **kwargs):
        
        order_product = self.logic.create(**request.data)
        order_id = order_product.order_id
        total_price = self.logic.get_total_price_by_order_id(order_id=order_id)
        
        note_logic = NoteLogic()
        note_logic.update_or_create(
            filters={'order_id': order_id},
            amount=total_price, 
            outstanding=total_price
        )
        data = self.logic.serialize(order_product)
        return Response(data, status=status.HTTP_201_CREATED)
