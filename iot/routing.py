# iot/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/sensor/(?P<room_name>[-\w]+)/$",
            consumers.SensorConsumer.as_asgi()),
]
