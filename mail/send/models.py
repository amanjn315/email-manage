from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True,unique=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=150)
    profile = models.TextField()

    def __str__(self):
        return self.name