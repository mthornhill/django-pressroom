from django.conf.urls import *
from models import Article
from feeds import LatestEntries
from pressroom.views import ArticleYearArchiveView, ArticleMonthArchiveView, ArticleDayArchiveView, ArticleDetailView
from views import SectionListView, ArticleArchiveIndexView
from api import ArticleResource

article_resource = ArticleResource()

# custom views
urlpatterns = patterns('pressroom.views',
    #url(r'^section/(?P<slug>[\-\d\w]+)/$', 'view_section', name="pr-section"),
    url(r'^section/(?P<slug>[\-\d\w]+)/$', SectionListView.as_view(),name="pr-section" ),
)

# articles
urlpatterns += patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<language>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/$', ArticleDetailView.as_view(slug_field='slug', queryset= Article.objects.get_published()), name='pr-article-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', ArticleDayArchiveView.as_view(date_field='pub_date', allow_empty=True, queryset= Article.objects.get_published()), name='pr-article-archive-day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', ArticleMonthArchiveView.as_view(date_field='pub_date', allow_empty=True, queryset= Article.objects.get_published()), name='pr-article-archive-month'),
    url(r'^(?P<year>\d{4})/$', ArticleYearArchiveView.as_view(date_field='pub_date', allow_empty=True, queryset= Article.objects.get_published(), make_object_list=True), name='pr-article-archive-year'),
    url(r'^$', ArticleArchiveIndexView.as_view(date_field='pub_date', allow_future=False, allow_empty=True, queryset= Article.objects.get_published()), name='pr-article-archive'),
)


# feeds
urlpatterns += patterns('',
    url(r'^latest/rss/$', LatestEntries(), name="pr-rss"),
    url(r'^api/', include(article_resource.urls)),
)
