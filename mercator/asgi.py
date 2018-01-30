import os

import dotenv
from channels.asgi import get_channel_layer


dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

channel_layer = get_channel_layer()
