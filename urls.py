from django.conf.urls.defaults import *

from pressroom.models import *
from tagging.models import Tag

# custom views
urlpatterns = patterns('pressroom.views',
    url(r'^$', 'index', name="pr-index"),
    url(r'^init/$', 'init', name="pr-init"),
    url(r'^section/(?P<slug>[\-\d\w]+)/$', 'view_section', name="pr-section")
)

# articles
article_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Article.objects.get_published()}
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^article/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'pub_date', 'slug_field': 'slug', 'queryset': Article.objects.all()}, name='pr-article-detail'),
    url(r'^article/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', article_args, name='pr-article-archive-day'),
    url(r'^article/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', article_args, name='pr-article-archive-month'),
    url(r'^article/(?P<year>\d{4})/$', 'archive_year', article_args, name='pr-article-archive-year'),
    url(r'^article/$', 'archive_index', article_args, name='pr-article-archive'),
)
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^article/page/(?P<page>[0-9]+)/$', 'object_list', {'queryset': Article.objects.get_published(), 'allow_empty': True, 'paginate_by': 3}, name='pr-article-list'),
)

# documents
document_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Document.objects.all()}
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^document/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', dict(document_args, slug_field='slug'), name='pr-document-detail'),
    url(r'^document/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', document_args, name='pr-document-archive-day'),
    url(r'^document/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', document_args, name='pr-document-archive-month'),
    url(r'^document/(?P<year>\d{4})/$', 'archive_year', document_args, name='pr-document-archive-year'),
    url(r'^document/$', 'archive_index', document_args, name='pr-document-archive'),
)
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^document/page/(?P<page>[0-9]+)/$', 'object_list', {'queryset': Document.objects.all(), 'allow_empty': True, 'paginate_by': 10}),
)

# galleries
gallery_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Gallery.objects.all()}
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'pub_date', 'slug_field': 'slug', 'queryset': Gallery.objects.all()}, name='pr-gallery-detail'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', gallery_args, name='pr-gallery-archive-day'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', gallery_args, name='pr-gallery-archive-month'),
    url(r'^gallery/(?P<year>\d{4})/$', 'archive_year', gallery_args, name='pr-gallery-archive-year'),
    url(r'^gallery/?$', 'archive_index', gallery_args, name='pr-gallery-archive'),
)
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^gallery/page/(?P<page>[0-9]+)/$', 'object_list', {'queryset': Gallery.objects.all(), 'allow_empty': True, 'paginate_by': 5}, name='pr-gallery-list'),
)

# photographs
photo_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Photo.objects.all()}
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'pub_date', 'slug_field': 'slug', 'queryset': Photo.objects.all()}, name='pr-photo-detail'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', photo_args, name='pr-photo-archive-day'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', photo_args, name='pr-photo-archive-month'),
    url(r'^photo/(?P<year>\d{4})/$', 'archive_year', photo_args, name='pr-photo-archive-year'),
    url(r'^photo/$', 'archive_index', photo_args, name='pr-photo-archive'),
)
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^photo/page/(?P<page>[0-9]+)/$', 'object_list', {'queryset': Photo.objects.all(), 'allow_empty': True, 'paginate_by': 10}),
)
