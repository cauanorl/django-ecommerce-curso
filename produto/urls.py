from django.urls import path
from . import views


app_name = 'produto'

urlpatterns = [
    path('', views.ListProducts.as_view(), name='lista'),
    path('search/', views.Search.as_view(), name='search'),
    path('<slug>', views.ProductDetails.as_view(), name='detalhe'),
    path('addtocart/', views.AddToCart.as_view(), name='adicionar'),
    path('removefromcart/<str:vid>', views.RemoveFromCart.as_view(), name='remover'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('summary/', views.Resume.as_view(), name='resumo'),
]
