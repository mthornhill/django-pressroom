from django import template
from django.db.models.loading import get_model
from pressroom.models import Article, PhotoSize


register = template.Library()


@register.inclusion_tag('pressroom/tag/latest_articles.html')
def latest_articles(count):
    return {'articles': Article.objects.all()[:count]}

@register.inclusion_tag('pressroom/tag/photo_block.html')
def photo_block(photo, size):
    size = photo._get_SIZE_size(size)
    return dict(photo=photo, size=size, image_url=getattr(photo, "get_%s_url" % size.name)())

@register.inclusion_tag('pressroom/tag/photo_block.html')
def inline_photo_block(photo, size):
    return dict(photo_block(photo, size), inline=True)

@register.inclusion_tag('pressroom/tag/teaser.html')
def teaser(article, h=2):
    return dict(article=article, h=h)

@register.inclusion_tag('pressroom/tag/photo_gallery.html')
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

@register.tag()
def object_set(parser, token):
    """ Retrieves a model queryset and makes it available to the current context

    Example usage:
    {% object_set pressroom.Article as article_set limit 5 %}

    """
    parts = token.split_contents()
    if len(parts) == 4:
        return ObjectSetNode(parts[1], parts[3])
    elif len(parts) == 6:
        return ObjectSetNode(parts[1], parts[3], parts[5])
    else:
        raise template.TemplateSyntaxError("%r tag requires 4 or 6 arguments." % token.contents[0])

class ObjectSetNode(template.Node):
    def __init__(self, model, context_name, limit=None):
        self.model = get_model(*model.split('.'))
        self.context_name = context_name
        self.limit = limit
    def render(self, context):
        if self.limit is None:
            context[self.context_name] = self.model.objects.all()
        else:
            context[self.context_name] = self.model.objects.all()[:limit]
        return ''
