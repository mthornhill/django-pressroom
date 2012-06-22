import random
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.contrib.webdesign.lorem_ipsum import paragraphs, sentence, words
from pressroom.models import Article

class PressroomTests(TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_environment(self):
        """Just make sure everything is set up correctly."""
        self.assert_(True)


    def test_published(self):

        headline = words(random.randint(5,10), common=False)

        a1, created = Article.objects.get_or_create( headline=headline,
            slug=slugify(headline),
            summary=sentence(),
            author=words(1,common=False),
            body=paragraphs(5),
            publish=True)

        a2, created = Article.objects.get_or_create( headline=headline,
            slug=slugify(headline),
            summary=sentence(),
            author=words(1,common=False),
            body=paragraphs(5),
            publish=False)


        published_articles = Article.objects.get_published()
        self.assertEqual(1, len(published_articles))

