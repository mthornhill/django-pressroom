from datetime import datetime

from django import template
from pressroom.models import Section, Article

register = template.Library()

@register.inclusion_tag('pressroom/includes/sections.html')
def show_sections():
    sections = Section.objects.all()
    return {'sections': sections}

@register.inclusion_tag('pressroom/includes/articles.html')
def show_articles():
    now = datetime.now()
    articles = Article.objects.get_published()
    return {'articles': articles}
