from django.urls import path
from . import views


app_name = 'perfil'

urlpatterns = [
    path('', views.FormLoginRegisterAndUpdateController.as_view(), name='login'),
    path('login/', views.FormLoginRegisterAndUpdateController.as_view(), name='login'),
    path('register/', views.FormLoginRegisterAndUpdateController.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]
