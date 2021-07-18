from rest_framework.response import Response
from rest_framework import status

from shipments.logic import ShipmentLogic
from ecommerce.core.views import BaseDetailView, BaseView
from ecommerce.views import BaseAPIView


class ShipmentView(BaseView):

    def __init__(self):
        super().__init__()

        self.logic = ShipmentLogic()


class ShipmentDetailView(BaseDetailView):
    
    def __init__(self):
        super().__init__()

        self.logic = ShipmentLogic()


class ConfirmShipmentView(BaseAPIView):
    
    def post(self, request, shipment_id, *args, **kwargs):
        
        ShipmentLogic().confirm_shipment(shipment_id=shipment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendShipmentView(BaseAPIView):
    
    def post(self, request, shipment_id, *args, **kwargs):
        
        ShipmentLogic().send_shipment(shipment_id=shipment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
