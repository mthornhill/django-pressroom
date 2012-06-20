#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import Image, ImageDraw
import random

from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.contrib.webdesign.lorem_ipsum import paragraphs, sentence, words
from django.contrib.sites.models import Site

from photologue.models import Photo, PhotoSize
from pressroom.models import Article

DIRNAME=os.path.dirname(__file__)

def load_data():
    
    site = Site.objects.all()[0]
    site.name = site.domain = "www.example.com"
    site.save()

    # photologue
    at = PhotoSize.objects.get_or_create(name='admin_thumbnail', width=100)
    display = PhotoSize.objects.get_or_create(name='display', width=400)
    fullsize = PhotoSize.objects.get_or_create(name='fullsize', width=600)
    thumbnail = PhotoSize.objects.get_or_create(name='thumbnail', width=120)

    photos = []
    for word in "make an image for each word in this sentence".split():
        ifn = generate_image(word)
        photo, created = Photo.objects.get_or_create(title=ifn, title_slug=slugify(ifn), is_public=True)
        photo.image.save(os.path.basename(ifn),
            ContentFile(open(ifn, 'rb').read()))
        photos.append(photo)


    # create 40 articles
    for i in range(1, 40):
        headline = words(random.randint(5,10))
        a, created = Article.objects.get_or_create(headline=headline, slug=slugify(headline), body=paragraphs(5), publish=True)

        for j in range(0, random.randint(0, 5)):
            a.photos.add(photos[j])



def generate_image(text):
    ''' A View that Returns a PNG Image generated using PIL'''

    size = (600,600)             # size of the image to create
    im = Image.new('RGB', size) # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
    # used to draw on the new image
    red = (255,0,0)    # color of our text
    text_pos = (10,10) # top-left position of our text
    # Now, we'll do the drawing:
    draw.text(text_pos, text, fill=red)

    del draw # I'm done drawing so I don't need this anymore

    filename = os.path.join(DIRNAME, 'images', text + '.png')
    fo = open(filename, 'wb')
    im.save(fo, 'PNG')
    fo.close()

    return filename


def run():    

    load_data()    
