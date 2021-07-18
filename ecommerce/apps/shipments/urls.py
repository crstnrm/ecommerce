from django.urls import path
from shipments import views

urlpatterns = [
    path('', views.ShipmentView.as_view()),
    path('<int:pk>/', views.ShipmentDetailView.as_view()),
    path('<int:shipment_id>/send/', views.SendShipmentView.as_view())
]
