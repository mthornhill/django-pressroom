from datetime import datetime

from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.views.generic import date_based, list_detail
from django.shortcuts import render_to_response
from tagging.models import TaggedItem

from pressroom.models import Article, Gallery, Photo, PhotoSize, Section


def init(request):
    sizes = {'square': (50, 50, True),
             'thumbnail': (100, 75, False),
             'inline': (220, 0, False),
             'feature': (320, 0, False),
             'display': (555, 0, False)}
    for name, params in sizes.iteritems():
        PhotoSize.objects.create(name=name,
                                 width = params[0],
                                 height = params[1],
                                 crop = params[2])
    sections = ['News', 'Announcements', 'Events']
    for section in sections:
        Section.objects.create(title=section, slug=section.lower())
    return HttpResponseRedirect('/admin/')


def index(request):
    articles = Article.objects.get_published()
    try:
        featured_story = articles.latest(field_name='pub_date')
        latest_stories = articles.exclude(pk=featured_story.id)[:5]
    except Article.DoesNotExist:
        featured_story = None
        latest_stories = None
    try:
        featured_photo = Photo.objects.latest(field_name='pub_date')
    except Photo.DoesNotExist:
        featured_photo = None
    latest_galleries = Gallery.objects.all()[:5]
    return render_to_response('pressroom/index.html', locals(),
                              context_instance=RequestContext(request))


def view_section(request, slug):
    section = Section.objects.get(slug__exact=slug)
    articles = section.articles.filter(publish=True, pub_date__lte=datetime.now())
    if articles.count():
        featured_story = articles.latest(field_name='pub_date')
        latest_stories = articles.exclude(pk=featured_story.id)[:5]
    latest_galleries = section.galleries.all()[:5]
    return render_to_response('pressroom/section.html', locals(),
                              context_instance=RequestContext(request))
