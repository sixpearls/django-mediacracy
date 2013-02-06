#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from mediacracy.views import load_static

urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', load_static, name='load_static'),
)
