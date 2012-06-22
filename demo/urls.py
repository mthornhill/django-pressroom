
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ajax_select import urls as ajax_select_urls

urlpatterns = patterns("",
    (r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^photos/', include('photologue.urls')),
    url(r'^imperavi/', include('imperavi.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'', include('pressroom.urls')),
)

urlpatterns += patterns("",
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )


try:
    from haystack.query import SearchQuerySet
    from haystack.views import FacetedSearchView
    from haystack.forms import FacetedSearchForm

    sqs = SearchQuerySet().facet('author').facet('sections')

    urlpatterns += patterns('haystack.views',
        url(r'^search/$', FacetedSearchView(
            template='search/search.html',
            searchqueryset=sqs,
            form_class=FacetedSearchForm
        ), name='haystack_search'),
    )
except ImportError, e:
    # haystack is optional
    pass