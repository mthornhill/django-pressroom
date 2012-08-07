from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import os
DIRNAME = os.path.dirname(__file__)

urlpatterns = patterns("",
    (r'', include('pressroom.urls')),
)

urlpatterns += patterns("",
    (r'^admin/(.*)', admin.site.root),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DIRNAME, "media"), 'show_indexes': True }),
)