"""
WSGI config for advitiya2k20 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv

load_dotenv('Advitiya-20/.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advitiya2k20.settings')

application = get_wsgi_application()
