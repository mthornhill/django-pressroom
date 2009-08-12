from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.comments.moderation import CommentModerator, moderator

from photologue.models import Gallery, Photo

from datetime import datetime
import os


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
    headline = models.CharField(max_length=200)
    slug = models.SlugField(help_text='A "Slug" is a unique URL-friendly title for an object.')
    summary = models.TextField(help_text="A single paragraph summary or preview of the article.")
    body = models.TextField("Body text")
    author = models.CharField(max_length=100)
    publish = models.BooleanField("Publish on site", default=True,
                                  help_text='Articles will not appear on the site until their "publish date".')
    sections = models.ManyToManyField('Section', related_name='articles')
    photos = models.ManyToManyField(Photo, related_name='articles', null=True, blank=True)
    documents = models.ManyToManyField('Document', related_name='articles', null=True, blank=True)
    enable_comments = models.BooleanField(default=True)

    # Custom article manager
    objects = ArticleManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
    
    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-article-detail', args=args)

class ArticleCommentModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'
    
    def moderate(self, comment, content_object, request):
        return True

if Article not in moderator._registry:
    moderator.register(Article, ArticleCommentModerator)

class Document(models.Model):
    file = models.FileField("Document", upload_to=PRESSROOM_DIR+"/documents/%Y/%b/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    summary = models.TextField()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

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
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField()

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pr-section', args=[self.slug])
