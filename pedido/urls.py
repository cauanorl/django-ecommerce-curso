from django.urls import path
from . import views


app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pay.as_view(), name='pagar'),
    path('saverequest/', views.SaveOrder.as_view(), name='salvarpedido'),
    path('list/', views.ListRequests.as_view(), name='lista'),
    path('finish/<int:pk>', views.FinishRequest.as_view(), name='finalizar'),
]
