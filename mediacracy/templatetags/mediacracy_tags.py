#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.loader import get_template#, select_template
from django.db.models.loading import get_model
from django.http import QueryDict
from urlparse import urlparse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=False)
def show_media(model_name='image',id=1,instance=None,**kwargs):
    """
    Renders massmedia media items using the template in mediacracy/tags/
    Lots of optional arguments can be passed

    {% show_media 'image' <pk> [file_size="< image_field >"] [fig_class="< class_name >"] %}

    where < image_field > is one of "thumbnail"/"small"/"medium"/"large"/"file"
    to set which image is loaded.

    {% show_media 'video' <pk> %}

    {% show_media 'collection' <pk> [columns="< num_columns >"] [make_links="True"] [show_title="True"] %}

    The columns argument adds a class "<num_columns>column" to the UL for styling. Defaults to 3
    The make_links argument renders an <a href> tag around the LI.
    The show_title argument renders the title before the UL.

    Image, Video, and Collection can take ``width="<width_attr>`` and ``height="<height_attr>"``
    optional arguments to set the image or iframe width/height attributes. For a 
    collection of images, they are passed onto the image renderer.

    """
    if instance is None:
        model = get_model('massmedia',model_name)
        instance = model.objects.get(id=id)

    c = template.Context({'media': instance})
    c.update(kwargs)
    if model_name=='image':
        show_image(instance,kwargs)
    elif (model_name=='video' or model_name=='collection') and instance.external_url:
        show_external_video(instance,kwargs)
        model_name = "external_video"
    elif model_name=='collection':
        show_collection(instance,kwargs)
    elif model_name=='document':
        show_document(instance,kwargs)

    t = get_template("mediacracy/tags/%s.html" % model_name)
    
    return mark_safe(t.render(c))

def show_external_video(instance,kwargs):
    parsed_url = urlparse(instance.external_url)
    if parsed_url.hostname.count('youtube'):
        BASE_URL = "http://www.youtube.com/embed/"
        query = QueryDict(parsed_url.query).copy()
        if query.get('v',None):
            kwargs.update({'video_url': BASE_URL + query['v'] })
        elif query.get('list',None):
            kwargs.update({'video_url': BASE_URL + "videoseries?list=" + query['list'] })
    elif parsed_url.hostname.count('vimeo'):
        video_id = parsed_url.path.split('/')[-1]
        kwargs.update({'video_url': 'http://player.vimeo.com/video/' + video_id + '?badge=0'})

def show_document(instance,kwargs):
    kwargs.update({'document_url': instance.file.url })
    if 'width' not in kwargs:
        kwargs.update({'width': "80%"})
    if 'height' not in kwargs:
        kwargs.update({'height': "500"})

def show_image(instance,kwargs):
    image_file_field = kwargs.pop('file_size','')
    try:
        kwargs.update({'media_src': getattr(instance,image_file_field).url })
    except:
        kwargs.update({'media_src': instance.media_url })

def show_collection(instance,kwargs):
    column_class = 'column'+kwargs.pop('columns',"3")
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
    kwargs.update({'items':items, 'column_class':column_class, })

