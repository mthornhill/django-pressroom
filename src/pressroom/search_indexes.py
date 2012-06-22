import datetime
import logging

from models import Article

try:
    from haystack import site
    from haystack import indexes

    class ArticleIndex(indexes.RealTimeSearchIndex):
        text = indexes.CharField(document=True, use_template=True)
        author = indexes.CharField(model_attr='author', faceted=True)
        sections = indexes.MultiValueField(faceted=True)
        pub_date = indexes.DateTimeField(model_attr='pub_date')

        def get_model(self):
            return Article


        def prepare_sections(self, object):
            section_names = []
            if object.sections.count() > 0:
                section_names = [s.title for s in object.sections.all()]
            #self.prepared_data['sections'] = section_names
            return section_names

        def index_queryset(self):
            """Used when the entire index for model is updated."""
            return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now()).filter(publish=True)

    site.register(Article, ArticleIndex)
except ImportError, e:
    logging.warning("Could not load haystack, pressroom article search disabled")