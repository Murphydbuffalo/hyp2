"""
ASGI config for web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from turbo.consumers import TurboStreamsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': TurboStreamsConsumer
})
