import os
from pathlib import Path

import dotenv
import django
from channels.routing import get_default_application

dotenv.read_dotenv(Path(__file__).resolve().parent.parent / '.env')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercator.settings.do")
django.setup()
application = get_default_application()
