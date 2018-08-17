from django.conf import settings
from django.db import models


class Card(models.Model):
    """カード"""

    name = models.CharField('カード名', max_length=200)
    image = models.CharField('画像', max_length=200)

    def __str__(self):
        return self.name
