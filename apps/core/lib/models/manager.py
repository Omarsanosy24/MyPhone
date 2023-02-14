from django.contrib.auth.models import UserManager
from django.db import models

class BaseUserManager(UserManager):
    ...


class SafeDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)

