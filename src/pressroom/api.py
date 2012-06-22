#from tastypie.authentication import BasicAuthentication
#from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from models import Article


class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.get_published()
        resource_name = 'pressroom/article'

        # Add it here.
        #authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()