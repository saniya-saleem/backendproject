from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
