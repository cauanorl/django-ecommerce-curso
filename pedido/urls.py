from django.urls import path
from . import views


app_name = 'pedido'

urlpatterns = [
    path('pagar/', views.Pay.as_view(), name='pagar'),
    path('fecharpedido/', views.CloseOrder.as_view(), name='fechar'),
    path('detalhe/<int:pk>', views.OrderDetails.as_view(), name='detalhe'),
]
