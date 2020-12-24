from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.CharField(max_length=1000)

    def __str__(self):
        return self.title