from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static
import os

# Create your models here.


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.name + '.' + ext
    foldername = 'events'
    return os.path.join(foldername, filename)


CATEGORY_CHOCIES = (
    ('1', 'Aeromodelling'),
    ('2', 'Finance'),
    ('3', 'Coding'),
    ('4', 'Robotics'),
    ('5', 'Automotive'),
    ('6', 'CAD'),
    ('7', 'Astronomy'),
    ('8', 'Gaming'),
    ('9', 'Quizzing'),
    ('10', 'Entrepreneurship'),
    ('11', 'Photo Editing'),
)


class Coordinator(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name + "\t"+self.phone


class Events(models.Model):

    category = models.CharField(max_length=20, choices=CATEGORY_CHOCIES)
    image = models.ImageField(
        upload_to=get_file_path, null=True, blank=True)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    venue = models.CharField(max_length=100)
    team_lower_limit = models.IntegerField()
    team_upper_limit = models.IntegerField()
    fees = models.IntegerField()
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    prize = models.IntegerField()
    rulebook = models.URLField()
    start_date_time = models.DateTimeField(blank=False)
    end_date_time = models.DateTimeField(blank=False)

    def __str__(self):
        return self.name+"\t"+self.coordinator.name
