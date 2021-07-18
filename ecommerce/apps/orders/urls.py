from django.urls import path
from orders import views

urlpatterns = [
    path('', views.OrderView.as_view()),
    path('<int:pk>/', views.OrderDetailView.as_view()),
]
