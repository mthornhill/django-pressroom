from django.conf.urls.defaults import *
from django_apps.pressroom.models import *

# custom views
urlpatterns = patterns('django_apps.pressroom.views',
    url(r'^$', 'index', name="pr-index"),
    url(r'^section/(?P<slug>[\-\d\w]+)/$', 'view_section', name="pr-section"),
    url(r'^section/(?P<slug>[\-\d\w]+)/page/(?P<page>[0-9]+)/$', 'view_section', name="pr-section-page")
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
