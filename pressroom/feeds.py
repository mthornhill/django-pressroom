from django.contrib.syndication.feeds import Feed
from models import Article

class LatestEntries(Feed):
    title = "Latest News"
    link = "/news/"
    description = "Updates on changes and additions"

    def items(self):
        return Article.objects.get_published().order_by('-pub_date')[:5]
