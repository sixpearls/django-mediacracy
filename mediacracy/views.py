#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib import admin
from django import forms

from django.utils.encoding import force_unicode
from django.contrib.admin.views.main import IS_POPUP_VAR

@login_required
def mediacracy_window(request):
    media = forms.Media(css = { 
            "all": ("mediacracy/jquery/jquery-ui.custom.css",)
        }, 
        js = (
            "mediacracy/js/jquery-1.8.2.min.js",
            "mediacracy/js/jquery-ui-1.10.0.custom.min.js",
            "mediacracy/js/jquery.form.min.js",
            "mediacracy/js/mediacracy_window.js",
            "mediacracy/js/mediacracy_ajax_csrf.js",
        ))

    model_list = []
    for model, model_admin in admin.site._registry.items():
        if 'massmedia' == model._meta.app_label:
            model_list.append({
                  'url_name': model._meta.module_name,
                  'read_name': force_unicode(model._meta.verbose_name_plural)
                })
    return render_to_response('mediacracy/mediacracy_window.html',
            {'model_list': model_list, 'media':media, 'is_popup': True, 'popup_var':IS_POPUP_VAR,},
            context_instance=RequestContext(request))