# python imports
from datetime import datetime
from django_extensions.db.fields import AutoSlugField
import os

# django imports
from django.conf import settings
from django.contrib.comments.moderation import CommentModerator, moderator
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


# other imports
from photologue.models import Gallery, Photo
from django_extensions.db.fields import ModificationDateTimeField, CreationDateTimeField, AutoSlugField, UUIDField
from taggit.managers import TaggableManager


# Get relative media path
try:
    PRESSROOM_DIR = settings.PRESSROOM_DIR
except:
    PRESSROOM_DIR = 'pressroom'

# define the models
class ArticleManager(models.Manager):
    def get_published(self):
        return self.filter(publish=True).filter(translation_of=None).order_by('-pub_date')
    def get_drafts(self):
        return self.filter(publish=False)

class Article(models.Model):
    headline = models.CharField(_("headline"),max_length=200)
    slug = models.SlugField(help_text=_('A "Slug" is a unique URL-friendly title for an object.'),
        unique_for_date="pub_date")
    summary = models.TextField(help_text=_("A single paragraph summary or preview of the article."), default=u"", null=True, blank=True)
    body = models.TextField(_("body text"))
    author = models.CharField(_("author"), max_length=100)
    pub_date = models.DateTimeField(_("publish date"), default=datetime.now)
    publish = models.BooleanField(_("publish on site"), default=True,
        help_text=_('Articles will not appear on the site until their "publish date".'))
    sections = models.ManyToManyField('Section', related_name='articles', verbose_name=_('sections'))
    photos = models.ManyToManyField(Photo, related_name='articles', null=True, blank=True, verbose_name=_('photos'))
    documents = models.ManyToManyField('Document', related_name='articles', null=True, blank=True, verbose_name=_('documents'))
    enable_comments = models.BooleanField(_('enable comments'),default=True)
    tags = TaggableManager(blank=True)

    language = models.CharField(_('language'), max_length=10, default=settings.LANGUAGE_CODE, choices=settings.LANGUAGES)
    translation_of = models.ForeignKey('self', verbose_name=_('translation_of'), null=True, blank=True, related_name='translations')

    modified = ModificationDateTimeField(verbose_name=_('modified'))
    modified_by = models.ForeignKey('auth.User', null=True, blank=True, editable=False, related_name="modified_by", verbose_name=_('modified_by'))
    created = CreationDateTimeField(verbose_name=_('created'))
    uid = UUIDField()

    # Custom article manager
    objects = ArticleManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%m/%d").lower().split("/") + [self.language, self.slug]
        return reverse('pr-article-detail', args=args)

class ArticleCommentModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'
    
    def moderate(self, comment, content_object, request):
        return True

if Article not in moderator._registry:
    moderator.register(Article, ArticleCommentModerator)

class Document(models.Model):
    file = models.FileField(_("document"), upload_to=PRESSROOM_DIR+"/documents/%Y/%b/%d")
    pub_date = models.DateTimeField(_("date published"), default=datetime.now)
    title = models.CharField(_('title'), max_length=200)
    slug = AutoSlugField(populate_from=('title',), help_text=_('A "Slug" is a unique URL-friendly title for an object.'))
    summary = models.TextField(_('summary'))

    modified = ModificationDateTimeField(verbose_name=_('modified'))
    created = CreationDateTimeField(verbose_name=_('created'))
    uid = UUIDField()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name = _('document')
        verbose_name_plural = _('documents')


    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-document-detail', args=args)
    
    def doc_dir(self):
        doc_dir = None
        if self.file is not None:
            doc_dir = os.path.dirname(self.file.path) 
        return doc_dir

    def delete(self):
        doc_dir = self.doc_dir()
        super(Document, self).delete()
        if doc_dir is not None:
            if os.listdir(doc_dir) == []:
                    os.removedirs(doc_dir)

class Section(models.Model):
    title = models.CharField(_('title'), max_length=80, unique=True)
    slug = AutoSlugField(populate_from=('title',), help_text=_('A "Slug" is a unique URL-friendly title for an object.'))

    modified = ModificationDateTimeField()
    created = CreationDateTimeField()
    uid = UUIDField()

    class Meta:
        ordering = ['title']
        verbose_name = _('section')
        verbose_name_plural = _('sections')


    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pr-section', args=[self.slug])
