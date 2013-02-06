#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', 'views.load_static', name='load_static'),
)
