from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from django.utils import timezone

from django.core.validators import MinLengthValidator, MaxLengthValidator, URLValidator

class Card(models.Model):
    # pk <-- auto
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(validators=[URLValidator])
    created_at = models.DateTimeField(default=timezone.now)
