import os
import zipfile
import StringIO

from datetime import datetime
import Image

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.functional import curry
from django.core.validators import ValidationError
from django.core.urlresolvers import reverse
from django.dispatch import dispatcher
from django.template.defaultfilters import slugify

from tagging.fields import TagField


# define our path roots
PRESSROOM_DIR = 'pressroom'
PRESSROOM_URL = '/pressroom'


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
    photos = models.ManyToManyField('Photo', related_name='articles', null=True, blank=True)
    documents = models.ManyToManyField('Document', related_name='articles', null=True, blank=True)
    tags = TagField(maxlength=255,
                    help_text="Tags may not contain spaces. Seperate multiple tags with a comma.")

    # Custom article manager
    objects = ArticleManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('headline', 'author', 'pub_date', 'publish', 'tags')
        list_filter = ['pub_date']
        save_as = True

    def __str__(self):
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
    tags = TagField(maxlength=255,
                    help_text="Tags may not contain spaces. Seperate multiple tags with a comma.")

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('title', 'pub_date', 'tags')
        list_filter = ['pub_date']

    def __str__(self):
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


class Gallery(models.Model):
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(maxlength=200)
    slug = models.SlugField(prepopulate_from=('title',),
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    sections = models.ManyToManyField('Section', related_name='galleries')
    photos = models.ManyToManyField('Photo', related_name='galleries')
    tags = TagField(maxlength=255,
                    help_text="Tags may not contain spaces. Seperate multiple tags with a comma.")

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name_plural = "galleries"

    class Admin:
        list_display = ('title', 'pub_date', 'tags', 'photo_count')
        list_filter = ['pub_date']
        date_hierarchy = 'pub_date'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-gallery-detail', args=args)


    def latest(self, limit=5):
        return self.photos.all()[:limit]

    def photo_count(self):
        return self.photos.all().count()
    photo_count.short_description = 'Count'


class GalleryUpload(models.Model):
    id = models.IntegerField(default=1, editable=False, primary_key=True)
    zip_file = models.FileField('Images file (.zip)', upload_to=PRESSROOM_DIR+"/temp")
    title_prefix = models.CharField(maxlength=75)
    caption = models.TextField()
    photographer = models.CharField(maxlength=100)
    info = models.TextField(blank=True,
                            help_text="Additional information about the photograph such as date taken, equipment used etc..")
    tags = models.CharField(maxlength=255,
                            help_text="Tags may not contain spaces. Seperate multiple tags with a comma.")

    class Admin:
        pass

    def save(self):
        super(GalleryUpload, self).save()
        self.process_zipfile()
        super(GalleryUpload, self).delete()

    def process_zipfile(self):
        if os.path.isfile(self.get_zip_file_filename()):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.get_zip_file_filename())
            bad_file = zip.testzip()
            if bad_file:
                raise forms.ValidationError('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 0
            gallery = Gallery.objects.create(title=self.title_prefix,
                                             slug=slugify(self.title_prefix),
                                             tags=self.tags)
            for filename in zip.namelist():
                data = zip.read(filename)
                title = ' '.join([self.title_prefix, str(count)])
                slug = slugify(title)
                photo = Photo(title=title, slug=slug,
                              caption=self.caption,
                              photographer=self.photographer,
                              info=self.info,
                              tags=self.tags)
                photo.save_image_file(filename, data)
                gallery.photos.add(photo)
                count = count + 1
            zip.close()


class Photo(models.Model):
    image = models.ImageField("Photograph", upload_to=PRESSROOM_DIR+"/photos/%Y/%b/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(maxlength=80)
    slug = models.SlugField(prepopulate_from=('title',),
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    caption = models.TextField()
    photographer = models.CharField(maxlength=100)
    info = models.TextField(blank=True,
                            help_text="Additional information about the photograph such as date taken, equipment used etc..")
    tags = TagField(maxlength=255,
                    help_text="Tags may not contain spaces. Seperate multiple tags with a comma.")

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('title', 'photographer', 'pub_date', 'tags', 'admin_thumbnail')
        list_filter = ['pub_date']
        list_per_page = 10

    def admin_thumbnail(self):
        if 'thumbnail' in [photosize.name for photosize in PhotoSize.objects.all()]:
            return '<a href="%s"><img src="%s"></a>' % \
                            (self.get_absolute_url(), self._get_SIZE_url('thumbnail'))
        else:
            return 'A "thumbnail" photo size has not been defined.'
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-photo-detail', args=args)


    def cache_path(self):
        return os.path.join(os.path.dirname(self.get_image_filename()), "cache")

    def image_url(self):
        return '/'.join([settings.MEDIA_URL, self.image.replace('\\', '/')])

    def cache_url(self):
        return '/'.join([os.path.dirname(self.image_url()), "cache"])

    def image_filename(self):
        return os.path.basename(self.image)

    def _get_filename_for_size(self, size):
        base, ext = os.path.splitext(self.image_filename())
        return ''.join([base, '_', size, ext])

    def _get_SIZE_size(self, size):
        return PhotoSize.objects.get(name__exact=size)

    def _get_SIZE_url(self, size):
        try:
            photosize = PhotoSize.objects.get(name=size)
        except PhotoSize.DoesNotExist:
            return ''
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return '/'.join([self.cache_url(), self._get_filename_for_size(photosize.name)])

    def _get_SIZE_path(self, size):
        try:
            photosize = PhotoSize.objects.get(name=size)
        except PhotoSize.DoesNotExist:
            return ''
        return os.path.join(self.cache_path(), self._get_filename_for_size(photosize.name))

    def add_accessor_methods(self, *args, **kwargs):
        for photosize in PhotoSize.objects.all():
            setattr(self, 'get_%s_size' % photosize.name, curry(self._get_SIZE_size, size=photosize.name))
            setattr(self, 'get_%s_url' % photosize.name, curry(self._get_SIZE_url, size=photosize.name))
            setattr(self, 'get_%s_path' % photosize.name, curry(self._get_SIZE_path, size=photosize.name))

    def size_exists(self, photosize):
        func = getattr(self, "get_%s_path" % photosize.name, None)
        if func is not None:
            if os.path.isfile(func()):
                return True
        return False

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        if not os.path.isdir(self.cache_path()):
            os.makedirs(self.cache_path())
        try:
            im = Image.open(self.get_image_filename())
        except IOError:
            return
        cur_width, cur_height = im.size
        new_width, new_height = photosize.size()
        if photosize.crop:
            ratio = float(new_width)/cur_width if cur_width < cur_height else \
                    float(new_height)/cur_height
            x = (cur_width * ratio)
            y = (cur_height * ratio)
            x_diff = abs((new_width - x) / 2)
            y_diff = abs((new_height - y) / 2)
            box = (x_diff, y_diff, (x-x_diff), (y-y_diff))
            resized = im.resize((x, y), Image.ANTIALIAS).crop(box)
        else:
            if not new_width == 0 and not new_height == 0:
                ratio = float(new_width)/cur_width if cur_width > cur_height else \
                        float(new_height)/cur_height
            else:
                if new_width == 0:
                    ratio = float(new_height)/cur_height
                else:
                    ratio = float(new_width)/cur_width
            resized = im.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.ANTIALIAS)
        resized.save(getattr(self, "get_%s_path" % photosize.name)())

    def remove_size(self, photosize, remove_dirs=True):
        if not self.size_exists(photosize):
            return
        filename = getattr(self, "get_%s_path" % photosize.name)()
        if os.path.isfile(filename):
            os.remove(filename)
        if remove_dirs:
            try:
                os.removedirs(self.cache_path())
            except:
                pass

    def remove_set(self):
        for photosize in PhotoSize.objects.all():
            self.remove_size(photosize, False)
            try:
                os.removedirs(self.cache_path())
            except:
                pass

    def save(self):
        super(Photo, self).save()

    def delete(self):
        super(Photo, self).delete()
        self.remove_set()


class PhotoSize(models.Model):
    name = models.CharField(maxlength=20, unique=True, help_text='Examples: "thumbnail", "display", "small"')
    width = models.PositiveIntegerField(default=0,
                                        help_text='Leave to size the image to the set height')
    height = models.PositiveIntegerField(default=0,
                                         help_text='Leave to size the image to the set width')
    crop = models.BooleanField("Crop photo to fit?", default=False,
                               help_text="If selected the image will be scaled \
                                         and cropped to fit the supplied dimensions.")

    class Meta:
        ordering = ['width', 'height']

    class Admin:
        list_display = ('name', 'width', 'height', 'crop')

    def __str__(self):
        return self.name

    def save(self):
        for photo in Photo.objects.all():
            photo.remove_size(self)
        super(PhotoSize, self).save()

    def delete(self):
        for photo in Photo.objects.all():
            photo.remove_size(self)
        super(PhotoSize, self).delete()

    def size(self):
        return (self.width, self.height)


class Section(models.Model):
    title = models.CharField(maxlength=80, unique=True)
    slug = models.SlugField(prepopulate_from=('title',))
    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['position']

    class Admin:
        list_display = ('title', 'position')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pr-section', args=[self.slug])


# Just a little instrospection...
# The following MUST come after the model definition.
def add_methods(sender, instance, signal, *args, **kwargs):
    """ Adds methods to access sized images (urls, paths)

    after the photo models __init__ function completes this method calls
    add_accessor_methods on each instance.

    """
    instance.add_accessor_methods()

# connect the add_accessor_methods function to the post_init signal
dispatcher.connect(add_methods, signal=signals.post_init, sender=Photo)
