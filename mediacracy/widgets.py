#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core import urlresolvers
from markitup.widgets import AdminMarkItUpWidget

# request.build_absolute_uri(urlresolvers.reverse('filebrowser:fb_browse'))

class TextifyMarkitupAdminWidget(AdminMarkItUpWidget):
    def _media(self):
        return super(TextifyMarkitupAdminWidget,self).media + 
          forms.Media(
            js=("%s" % urlresolvers('load_static',args=['constant_preview_refresh.js']),
              )
            )
    media = property(_media)