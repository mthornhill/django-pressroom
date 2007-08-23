import os
import zipfile
import StringIO

from datetime import datetime
import Image

from django.db import models
from django.db.models import signals
from django.db.models.loading import AppCache
from django.conf import settings
from django.utils.functional import curry
from django.core.validators import ValidationError
from django.core.urlresolvers import reverse
from django.dispatch import dispatcher
from django.template.defaultfilters import slugify

from django_apps.photologue.models import Gallery, Photo


# Get relative media path
try:
    PRESSROOM_DIR = settings.PRESSROOM_DIR
except:
    PRESSROOM_DIR = 'pressroom'


# define the models
class ArticleManager(models.Manager):
    def get_published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now)
    def get_drafts(self):
        return self.filter(publish=False)

class Article(models.Model):
    pub_date = models.DateTimeField("Publish date", default=datetime.now)
    headline = models.CharField(maxlength=200)
    slug = models.SlugField(prepopulate_from=("headline",),
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    summary = models.TextField(help_text="A single paragraph summary or preview of the article.")
    body = models.TextField("Body text")
    author = models.CharField(maxlength=100)
    publish = models.BooleanField("Publish on site", default=True,
                                  help_text='Articles will not appear on the site until their "publish date".')
    sections = models.ManyToManyField('Section', related_name='articles')
    photos = models.ManyToManyField(Photo, related_name='articles', null=True, blank=True)
    documents = models.ManyToManyField('Document', related_name='articles', null=True, blank=True)

    # Custom article manager
    objects = ArticleManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('headline', 'author', 'pub_date', 'publish')
        list_filter = ['pub_date']
        save_as = True

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-article-detail', args=args)


class Document(models.Model):
    file = models.FileField("Document", upload_to=PRESSROOM_DIR+"/documents/%Y/%b/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(maxlength=200)
    slug = models.SlugField(prepopulate_from=('title',))
    summary = models.TextField()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('title', 'pub_date')
        list_filter = ['pub_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-document-detail', args=args)

    def doc_dir(self):
        return os.path.dirname(self.get_file_filename())

    def remove_dirs(self):
        if os.path.isdir(self.doc_dir()):
            if os.listdir(self.doc_dir()) == []:
                os.removedirs(self.doc_dir())

    def delete(self):
        super(Document, self).delete()
        self.remove_dirs()


class Section(models.Model):
    title = models.CharField(maxlength=80, unique=True)
    slug = models.SlugField(prepopulate_from=('title',))

    class Meta:
        ordering = ['title']

    class Admin:
        list_display = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pr-section', args=[self.slug])


# Add the TagFields to models if django-tagging is found.
if "tagging" in AppCache().app_models:
    try:
        from tagging.fields import TagField
    except ImportError:
        pass
    else:
        tag_field = TagField(help_text="Tags may not contain spaces. Seperate \
                                        multiple tags with a space or comma.")
        Article.add_to_class('tags', tag_field)
        Document.add_to_class('tags', tag_field)
