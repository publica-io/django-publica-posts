# -*- coding: utf-8 -*-
from django.conf import settings


USE_POSTS_MODEL = getattr(settings, 'POSTS_USE_POSTS_MODEL', True)
