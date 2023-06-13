from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"
    

class Project(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(max_length=4)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} - {self.artist}"
