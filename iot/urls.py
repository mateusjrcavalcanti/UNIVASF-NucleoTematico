from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('sensors/', views.sensors, name='sensors'),
    path('sensors/<str:sensor_id>/', views.sensors, name='sensor'),
]
