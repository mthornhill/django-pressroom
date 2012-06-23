from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import dates

from models import Section
from pressroom.models import Article

class SectionListView(ListView):
    template_name = "pressroom/view_section.html"
    def get_queryset(self):
        self.section = get_object_or_404(Section, slug__iexact=self.kwargs['slug'])
        return self.section.articles.filter(publish=True, pub_date__lte=datetime.now())


class CurrentLanguageMixin(object):
    """
    To be subclassed by date generic views
    * Add default params to article listings
    * Allow article lists to be further filtered by category
    From: http://martinogden.me/2011/03/27/quick-look-django-13-class-based-views/
    """
    date_field = 'published_at'
    paginate_by = 10
    allow_empty = True
    queryset = Article.objects.get_published()
    month_format = "%m"

    def get_queryset(self):
        # we only get LANGUAGE_CODE if we have 'django.middleware.locale.LocaleMiddleware', in middleware
        if hasattr(self.request, 'LANGUAGE_CODE'):
            return Article.objects.filter(publish=True).filter(language=self.request.LANGUAGE_CODE)

        return super(CurrentLanguageMixin, self).get_queryset()

class ArticleArchiveIndexView(CurrentLanguageMixin, dates.ArchiveIndexView):
    pass

class ArticleYearArchiveView(CurrentLanguageMixin, dates.YearArchiveView):
    pass

class ArticleMonthArchiveView(CurrentLanguageMixin, dates.MonthArchiveView):
    pass

class ArticleDayArchiveView(CurrentLanguageMixin, dates.DayArchiveView):
    pass

class ArticleDetailView(DetailView):
    def get_queryset(self):
        # we allow viewing of any article no matter what the current language code
        return Article.objects.filter(publish=True)
