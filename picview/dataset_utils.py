__author__ = 'derpson'

from django.db import transaction
from .models import Picture, PictureTag
from random import sample, randint

MIN_TAGS = 0
MAX_TAGS = 10

MIN_LIKES = 0
MAX_LIKES = 50

@transaction.atomic
def tag_pictures(drop_existing=True):
    pictures = Picture.objects.iterator()
    tags = PictureTag.objects.all()
    if drop_existing:
        for t in tags:
            t.tagLinks.clear()
    for picture in pictures:
        count = tags.count()
        rand_ids = sample(xrange(1, count), randint(MIN_TAGS, MAX_TAGS))
        chosen_tags = tags.filter(id__in=rand_ids)
        for ct in chosen_tags:
            ct.tagLinks.add(picture)

@transaction.atomic
def place_likes():
    pictures = Picture.objects.iterator()
    for picture in pictures:
        picture.userLikes = randint(MIN_LIKES, MAX_LIKES)
        picture.save()