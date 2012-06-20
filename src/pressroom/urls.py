from datetime import datetime

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, DayArchiveView, MonthArchiveView

from models import Article
from feeds import LatestEntries
from views import SectionListView


# custom views
urlpatterns = patterns('pressroom.views',
    #url(r'^section/(?P<slug>[\-\d\w]+)/$', 'view_section', name="pr-section"),
    url(r'^section/(?P<slug>[\-\d\w]+)/$', SectionListView.as_view(),name="pr-section" ),
)

# articles
urlpatterns += patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', DetailView.as_view(slug_field='slug', queryset= Article.objects.get_published()), name='pr-article-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', DayArchiveView.as_view(date_field='pub_date', paginate_by=10, allow_empty=True, queryset= Article.objects.get_published()), name='pr-article-archive-day'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', MonthArchiveView.as_view(date_field='pub_date', paginate_by=10, allow_empty=True, queryset= Article.objects.get_published()), name='pr-article-archive-month'),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(date_field='pub_date', paginate_by=10, allow_empty=True, queryset= Article.objects.get_published(), make_object_list=True), name='pr-article-archive-year'),
    url(r'^$', ArchiveIndexView.as_view(date_field='pub_date', paginate_by=10, allow_future=False, allow_empty=True, queryset= Article.objects.get_published()), name='pr-article-archive'),
)


# feeds
urlpatterns += patterns('',
    url(r'^latest/rss/$', LatestEntries(), name="pr-rss"),
)
