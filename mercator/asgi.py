import os
from pathlib import Path

import dotenv
import django
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from mercator.routing import ws_routes

dotenv.read_dotenv(Path(__file__).resolve().parent.parent / '.env')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercator.settings.do")
django.setup()

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': ws_routes
})
