from typing import List

from django.core.exceptions import ValidationError
from django.db import transaction
from utils import communications

from orders.logic import OrderLogic
from shipments.constants import (
    ShipmentProductStatus,
    ShipmentStatus,
)
from shipments.models import Shipment, ShipmentProduct
from ecommerce.core.logic import BaseLogic


class ShipmentLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = Shipment

    def create(self, order_id: int, **kwargs) -> Shipment:

        order_logic = OrderLogic()
        order = order_logic.get(id=order_id)
        if not (order.is_paid or order.is_partial_shipment):
            raise ValidationError(f'Order {order_id} can not be shipped.')

        return super().create(order_id=order_id, **kwargs)

    def send_shipment(self, shipment_id:int) -> None:
        
        shipment = self.get(id=shipment_id)
        if shipment.status != ShipmentStatus.CREATED.value:
            raise ValidationError(
                f'Shipment {shipment_id} can not be shipped.'
            )
            
        shipment = self.update(
            instance=shipment, 
            status=ShipmentStatus.SENT.value
        )
        self.update_products_status_by_shipment(
            shipment=shipment, 
            status=ShipmentProductStatus.SENT.value
        )

        products = shipment.products.all()

        order_logic = OrderLogic()
        order_logic.send_order(
            order_id=shipment.order_id, 
            num_of_products_shipped=len(products)
        )

        to = None
        template = None
        communications.send_communication(to=to, template=template)

    def confirm_shipment(self, shipment_id: int) -> None:

        shipment = self.get(id=shipment_id)
        shipment = self.update(
            instance=shipment, 
            status=ShipmentStatus.COMPLETED.value
        )

        self.update_products_status_by_shipment(
            shipment=shipment, 
            status=ShipmentProductStatus.RECEIVED.value
        )

        order_logic = OrderLogic()
        order_logic.confirm_order(order_id=shipment.order_id)

        to = None
        template = None
        communications.send_communication(to=to, template=template)

    def update_products_status_by_shipment(
        self, 
        shipment: Shipment, 
        status: int
    ) -> None:

        products = shipment.products.all()
        for product in products:
            product.status = status

        shipment_product_logic = ShipmentProductLogic()
        shipment_product_logic.bulk_update(objs=products, fields=['status'])


class ShipmentProductLogic(BaseLogic):
    
    def __init__(self):
        super().__init__()

        self.model = ShipmentProduct
    
    @transaction.atomic
    def create(
        self, shipment_id: int, product_id: int, **kwargs
    ) -> ShipmentProduct:
        
        shipment_logic = ShipmentLogic()
        shipment = shipment_logic.get(pk=shipment_id)

        is_product_already_shipped = self.find(
            shipment_id=shipment_id, 
            product_id=product_id
        ).exists()
        if is_product_already_shipped:
            raise ValidationError(
                f'The product {product_id} by order'
                f' {shipment.order_id} is already shipped.'
            )

        return super().create(**kwargs)

    def bulk_update(
        self, objs: List[ShipmentProduct], fields: List[str]
    ) -> List[ShipmentProduct]:

        return self.model.objects.bulk_update(objs, fields=fields)
