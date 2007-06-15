from django import template
from cbc_website.pressroom.models import Article, PhotoSize


register = template.Library()


@register.inclusion_tag('pressroom/tag/latest_articles.html')
def latest_articles(count):
    return {'articles': Article.objects.all()[:count]}

def photo_block(photo, size):
    size = photo._get_SIZE_size(size)
    return dict(photo=photo, size=size, image_url=getattr(photo, "get_%s_url" % size.name)())

def inline_photo_block(photo, size):
    return dict(photo_block(photo, size), inline=True)

def teaser(article, h=2):
    return dict(article=article, h=h)

def photo_gallery(gallery, limit=None):
    if limit:
        photos = gallery.photos.all()[:limit]
    else:
        photos = gallery.photos.all()
    return dict(gallery=gallery, photos=photos)

@register.inclusion_tag('pressroom/tag/item_list.html')
def gallery_list(photo):
    return {'label': 'This photo belongs to these galleries',
            'items': [{'name': gallery.title, 'url': gallery.get_absolute_url()} for gallery in photo.galleries.all()]}

@register.inclusion_tag('pressroom/tag/item_list.html')
def size_list(photo):
    items = [{'name': 'original', 'url': photo.get_image_url()}]
    return {'label': 'This photo is available in these sizes',
            'items': items + [{'name': photosize.name, 'url': getattr(photo, "get_%s_url" % photosize.name)()} for photosize in PhotoSize.objects.all()]}

photo_block = register.inclusion_tag('pressroom/tag/photo_block.html')(photo_block)
inline_photo_block = register.inclusion_tag('pressroom/tag/photo_block.html')(inline_photo_block)
teaser = register.inclusion_tag('pressroom/tag/teaser.html')(teaser)
photo_gallery = register.inclusion_tag('pressroom/tag/photo_gallery.html')(photo_gallery)
