#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.db.models.loading import get_model
from django.utils.safestring import mark_safe

register = template.Library()

def do_show_media(parser, token):
    args = token.split_contents()[1:]

    return ShowMediaNode(*args)

class ShowMediaNode(template.Node):
    def __init__(self, *args):
        model_name = args[0]
        pk = args[1]
        model = get_model('massmedia',model_name)
        self.instance = model.objects.get(pk=pk)
        self.other_args = args[2:]

    def render(self, context):
        output = self.instance.render_detail()
        print output
        return output

register.tag('show_media', do_show_media)