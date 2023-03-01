
import os
from django.urls import path
from Security_Testing.consumers import SecurityConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DW.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter([path(r"ws/sqlinjection", SecurityConsumer.as_asgi())]),
    }
)

