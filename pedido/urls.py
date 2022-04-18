from django.urls import path
from . import views


app_name = 'pedido'

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pagar'),
    path('saverequest/', views.SaveOrder.as_view(), name='salvarpedido'),
    path('list/', views.ListOrders.as_view(), name='lista'),
    path('detail/<int:pk>', views.DetailOrder.as_view(), name='detalhe'),
]
