from django.urls import path
from . import views


app_name = 'perfil'

urlpatterns = [
    path('', views.Register.as_view(), name='registrar'),
    path('update/', views.Update.as_view(), name='atualizar'),
    path('login/', views.Update.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]
