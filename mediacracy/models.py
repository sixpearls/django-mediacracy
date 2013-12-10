#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.db.models.signals import class_prepared, pre_delete
from django.utils.translation import ugettext, ugettext_lazy as _
import mimetypes
import os

from mediacracy import settings

from django import template
template.add_to_builtins('mediacracy.templatetags.mediacracy_tags')

def add_image_fields(sender, **kwargs):
    """
    class_prepared signal handler that checks for the model massmedia.Image
    and adds sized image fields
    """
    if sender.__name__ == "Image" and sender._meta.app_label == 'massmedia':
        large = models.ImageField(upload_to=".", blank=True, verbose_name=_('large image file'))
        medium = models.ImageField(upload_to=".", blank=True, verbose_name=_('medium image file'))
        small = models.ImageField(upload_to=".", blank=True, verbose_name=_('small image file'))
        
        large.contribute_to_class(sender, "large")
        medium.contribute_to_class(sender, "medium")
        small.contribute_to_class(sender, "small")

class_prepared.connect(add_image_fields) 

from massmedia.models import Image
from PIL import Image as PILImage, ImageFile as PILImageFile
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from massmedia.settings import IMAGE_UPLOAD_TO
from time import strftime

try:
    Image._meta.get_field_by_name('large')[0]
except:
    add_image_fields(Image)

Image.image_fields = [
    Image._meta.get_field_by_name('file')[0],
    Image._meta.get_field_by_name('large')[0],
    Image._meta.get_field_by_name('medium')[0],
    Image._meta.get_field_by_name('small')[0],
    Image._meta.get_field_by_name('thumbnail')[0],]

def resize(file_name, size):
    new_image = PILImage.open(file_name)
    new_image.thumbnail( size, PILImage.ANTIALIAS)
    temp_handle = StringIO()

    name,ext = os.path.splitext( os.path.basename(file_name) )

    ct = mimetypes.types_map[ext]
    fmt = PILImage.EXTENSION[ext]

    try:
        new_image.save(temp_handle, format=fmt, optimize=True)
    except:
        original_block = PILImageFile.MAXBLOCK
        PILImageFile.MAXBLOCK = new_image.size[0] * new_image.size[1]
        new_image.save(temp_handle, format=fmt, optimize=True)
        PILImageFile.MAXBLOCK = original_block

    del new_image
    temp_handle.seek(0)
    thumbname = name + '_' + '_'.join([str(x) for x in size]) + '.' + ext
    suf = SimpleUploadedFile(thumbname, temp_handle.read(), content_type=ct)
    return suf

def image_generate_thumbnails(self):
    if self.external_url:
        import urllib
        from urlparse import urlparse
        filepath, headers = urllib.urlretrieve(self.external_url)
        image = PILImage.open(filepath)
        filename = os.path.basename(urlparse(self.external_url).path)
    elif self.file:
        image = PILImage.open(self.file.path)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGBA')

    try:
        this_path = os.path.split(self.file.name)[0]+'/'
    except:
        this_path = strftime(IMAGE_UPLOAD_TO)+'/'

    original_width, original_height = image.size
    del image
    
    for (field_name,size) in settings.IMAGE_SIZES.items():
        image_field = getattr(self,field_name,None)
        if image_field is not None:
            if (original_width > size[0] or original_height > size[1]): 
                suf = resize(self.file.path, size)
                preferredname = this_path+suf.name
                if (image_field.storage.exists(preferredname)):
                    image_field.storage.delete(preferredname)
                newname = image_field.storage.get_available_name(preferredname)
                image_field.storage.save(name=newname,content=suf)#,save=False)
                image_field.name = newname #okay
            else:
                image_field.name = self.file.name

def image_delete_files(self):
    for field in self.image_fields:
        field_ref = getattr(self,field.name)
        try:
            field_ref.delete(save=False)
        except:
            pass

def image_save(self):
    do_generate_thumbs = False
    if self.pk is not None:
        this = type(self).objects.get(pk=self.pk)
        if os.path.basename(self.file.name) != os.path.basename(this.file.name):
            this._delete_files()
            do_generate_thumbs = True
    else:
        do_generate_thumbs = True
    super(Image, self).save()
    if do_generate_thumbs:
        self._generate_thumbnails()
        super(Image, self).save()

Image._generate_thumbnails = image_generate_thumbnails
Image.save = image_save
Image._delete_files = image_delete_files

def delete_image_files(sender,instance,*args,**kwargs):
    if sender.__name__ == "Image" and sender._meta.app_label == 'massmedia':
        instance._delete_files()
pre_delete.connect(delete_image_files)