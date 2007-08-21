from datetime import datetime

from django.template.context import RequestContext
from django.views.generic import list_detail
from django.shortcuts import render_to_response

from django_apps.photologue.models import Gallery
from django_apps.pressroom.models import Article, Section


def index(request):
    articles = Article.objects.get_published()[:3]
    galleries = Gallery.objects.all()[:3]
    return render_to_response('pressroom/index.html', locals(),
                              context_instance=RequestContext(request))


def view_section(request, slug, page=1):
    section = Section.objects.get(slug__exact=slug)
    articles = section.articles.filter(publish=True, pub_date__lte=datetime.now())
    return list_detail.object_list(request,
                                   queryset=articles,
                                   paginate_by=5,
                                   page=page,
                                   allow_empty=True,
                                   template_name='pressroom/view_section.html',
                                   extra_context={'section': section,
                                                  'galleries': Gallery.objects.all()[:3]})
