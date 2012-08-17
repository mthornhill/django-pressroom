import random
from django.contrib.webdesign.lorem_ipsum import words, sentence, paragraphs
from django.template.defaultfilters import slugify
from django.test import TestCase
from pressroom.models import Article

class PressroomTests(TestCase):
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


    def test_canonical_published(self):

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
            publish=True)

        self.assertEqual(2, len(Article.objects.get_published()))

        # set a2 to be a translation of a1
        a2.translation_of = a1
        a2.save()

        # we only expect 1 canonical object now as a2 is a translation of a1
        self.assertEqual(1, len(Article.objects.get_published()))



