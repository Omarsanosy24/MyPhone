from apps.core.lib import models


class Customer(models.Model):
    name = models.CharField(
        max_length=128,
    )
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.address})"
