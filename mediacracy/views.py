#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.http import require_http_methods

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.http import require_http_methods
from django.template import RequestContext, loader

def load_static(request,path=''):
    return render_to_response('mediacracy/%s' % path,{'session': request.session,},
            context_instance=RequestContext(request))
