#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.core import urlresolvers
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from markitup.widgets import AdminMarkItUpWidget, MarkItUpWidget

class TextifyMarkitupAdminWidget(AdminMarkItUpWidget):
    def render(self,*args,**kwargs):
        attrs_copy = kwargs['attrs'].copy()

        html = super(MarkItUpWidget,self).render(*args,**kwargs)
        html += '<script type="text/javascript">'
        html += render_to_string('mediacracy/markitup_helper.js',{ 'id': attrs_copy['id'] })
        html += '</script>'

        return mark_safe(html)
    
    def _media(self):
        return super(TextifyMarkitupAdminWidget,self).media + forms.Media(
            css={'all': ('mediacracy/markitup/markitup_helper.css',),},
            js=("mediacracy/js/mediacracy_ajax_csrf.js",)
            )
    media = property(_media)
