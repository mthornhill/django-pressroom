from django.conf.urls.defaults import *
from django.conf import settings

from ajax_select import urls as ajax_select_urls

from django.contrib import admin
admin.autodiscover()

import os
DIRNAME = os.path.dirname(__file__)

urlpatterns = patterns("",
    (r'^admin/lookups/', include(ajax_select_urls)),
    (r'', include('pressroom.urls')),
    url(r'^photos/', include('photologue.urls')),
    url(r'^imperavi/', include('imperavi.urls')),
    (r'^search/', include('haystack.urls')),
)

urlpatterns += patterns("",
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )