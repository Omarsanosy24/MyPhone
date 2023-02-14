from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

from apps.core.lib import models
from apps.core.lib.models.manager import BaseUserManager


class User(models.Model, AbstractUser):
    objects = BaseUserManager()
    history = HistoricalRecords()
