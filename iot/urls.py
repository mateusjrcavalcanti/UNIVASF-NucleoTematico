# iot/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sensors/", views.index, name="sensors"),
    path('send/', views.tcpSend, name='tcp_send'),
    path("sensor/<str:room_name>/", views.room, name="room"),
]
