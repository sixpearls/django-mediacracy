#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.loader import get_template#, select_template
from django.db.models.loading import get_model
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=False)
def show_media(model_name='image',id=1,instance=None,**kwargs):
    if instance is None:
        model = get_model('massmedia',model_name)
        instance = model.objects.get(id=id)
    t = get_template("mediacracy/tags/%s.html" % model_name)
    c = template.Context({'media': instance})
    if model_name=='image':
        show_image(instance,kwargs)
    if model_name=='collection':
        show_collection(instance,kwargs)
    c.update(kwargs)
    return mark_safe(t.render(c))

def show_image(instance,kwargs):
    image_file_field = kwargs.pop('file_size','')
    try:
        kwargs.update({'media_src': getattr(instance,image_file_field).url })
    except:
        kwargs.update({'media_src': instance.media_url })

def show_collection(instance,kwargs):
    use_hrefs = kwargs.pop('use_hrefs',False)
    items = []
    for item_rel in instance.collectionrelation_set.all():
        item = item_rel.content_object
        items.append({
            'content':show_media(
                model_name=item._meta.module_name,
                instance=item,
                **kwargs),
            'url': item.get_absolute_url(),
            'title': item.title,
            })
    kwargs.update({'items':items, 'use_hrefs':use_hrefs})

