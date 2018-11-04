from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from django.utils import timezone

from django.core.validators import MinLengthValidator, MaxLengthValidator, URLValidator

class UserDecks(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_source = models.URLField(validators=[URLValidator])
    name = models.CharField('デッキ名', max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} , {}".format(self.owner, self.name)

class Deck(models.Model):

    name = models.ForeignKey(UserDecks, on_delete=models.CASCADE)
    card_source = models.URLField(validators=[URLValidator])


class Card(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('カード名', max_length=255, blank=True)
    card_source = models.URLField(validators=[URLValidator])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
