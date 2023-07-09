from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100)
    ext_id = models.CharField(max_length=100, unique=True, null=True)

    def get_projects_list(self):
        return list(self.projects.all())

    def __str__(self) -> str:
        return f"{self.name}"
    

class Project(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='projects')
    ext_id = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.artist}"
