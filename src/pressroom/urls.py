from django.conf import settings
from django.conf.urls.defaults import *
from pressroom.models import *
from pressroom.feeds import LatestEntries


try:
    MAKE_ARTICLE_OBJECT_LIST = settings.PRESSROOM_MAKE_ARTICLE_OBJECT_LIST
except:
    MAKE_ARTICLE_OBJECT_LIST = False

try:
    MAKE_DOCUMENT_OBJECT_LIST = settings.PRESSROOM_MAKE_DOCUMENT_OBJECT_LIST
except:
    MAKE_DOCUMENT_OBJECT_LIST = False

# custom views
urlpatterns = patterns('pressroom.views',
    url(r'^$', 'index', name="pr-index"),
    url(r'^section/(?P<slug>[\-\d\w]+)/$', 'view_section', name="pr-section"),
    url(r'^section/(?P<slug>[\-\d\w]+)/page/(?P<page>[0-9]+)/$', 'view_section', name="pr-section-page"),
    url(r'^article/page/(?P<page>[0-9]+)/$', 'article_list', name='pr-article-list'),
)

# articles
article_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Article.objects.get_published()}
if MAKE_ARTICLE_OBJECT_LIST:
    year_article_args = dict(article_args, make_object_list=True)
else:
    year_article_args = article_args

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^article/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+).html$', 'object_detail', {'date_field': 'pub_date', 'slug_field': 'slug', 'queryset': Article.objects.all()}, name='pr-article-detail'),
    url(r'^article/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', article_args, name='pr-article-archive-day'),
    url(r'^article/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', article_args, name='pr-article-archive-month'),
    url(r'^article/(?P<year>\d{4})/$', 'archive_year', year_article_args, name='pr-article-archive-year'),
    url(r'^article/$', 'archive_index', article_args, name='pr-article-archive'),
)

# documents
document_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Document.objects.all()}
if MAKE_ARTICLE_OBJECT_LIST:
    year_document_args = dict(document_args, make_object_list=True)
else:
    year_document_args = document_args
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^document/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'pub_date', 'slug_field': 'slug', 'queryset': Document.objects.all()}, name='pr-document-detail'),
    url(r'^document/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', document_args, name='pr-document-archive-day'),
    url(r'^document/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', document_args, name='pr-document-archive-month'),
    url(r'^document/(?P<year>\d{4})/$', 'archive_year', year_document_args, name='pr-document-archive-year'),
    url(r'^document/$', 'archive_index', document_args, name='pr-document-archive'),
)
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^document/page/(?P<page>[0-9]+)/$', 'object_list', {'queryset': Document.objects.all(), 'allow_empty': True, 'paginate_by': 20}, name='pr-document-list'),
)

feeds = {
    'rss': LatestEntries,
}

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',  {'feed_dict': feeds}, name="pr-rss"),
)

