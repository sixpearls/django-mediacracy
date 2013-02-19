#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

DEFAULT_IMAGE_SIZES = {
    'large': 1024,
    'medium': 600,
    'small': 300,
    'thumbnail': 150,
}

DEFAULT_SETTINGS = {
    'IMAGE_SIZES': DEFAULT_IMAGE_SIZES,
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'MEDIACRACY_SETTINGS', {}))

globals().update(USER_SETTINGS)
