#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_IMAGE_SIZES = {
    'large': (1024,1024),
    'medium': (600,600),
    'small': (300,300),
    'thumbnail': (150,150),
}

DEFAULT_SETTINGS = {
    'IMAGE_SIZES': DEFAULT_IMAGE_SIZES,
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()

USER_SETTINGS.update(getattr(settings, 'MEDIACRACY_SETTINGS', {}))

for size in USER_SETTINGS['IMAGE_SIZES']:
    if type(USER_SETTINGS['IMAGE_SIZES'][size]) is int:
        USER_SETTINGS['IMAGE_SIZES'][size] = (USER_SETTINGS['IMAGE_SIZES'][size],USER_SETTINGS['IMAGE_SIZES'][size],)

    elif len(USER_SETTINGS['IMAGE_SIZES'][size]) != 2 or type(USER_SETTINGS['IMAGE_SIZES'][size][0]) is not int or type(USER_SETTINGS['IMAGE_SIZES'][size][1]) is not int:
        raise ImproperlyConfigured('IMAGE_SIZES["%s"] should be an integer or 2-element list or tuple of integers' % size)

globals().update(USER_SETTINGS)
