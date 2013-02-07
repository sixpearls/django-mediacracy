#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.utils.translation import ugettext, ugettext_lazy as _

from mediacracy import settings

from django import template
template.add_to_builtins('mediacracy.templatetags.mediacracy_tags')