#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from mediacracy.views import mediacracy_window

urlpatterns = patterns('',
    url(r'^window/$', mediacracy_window, name='mediacracy_window'),
)
