from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.crypto import get_random_string
import os
import string
from ca.models import Profile

# Create your models here.


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.name + '.' + ext
    foldername = 'events'
    return os.path.join(foldername, filename)


CATEGORY_CHOCIES = (
    ('1', 'Aeromodelling'),
    ('7', 'Astronomy'),
    ('5', 'Automotive'),
    ('6', 'CAD'),
    ('3', 'Coding'),
    ('10', 'Entrepreneurship'),
    ('2', 'Finance'),
    ('8', 'Gaming'),
    ('11', 'Photo Editing'),
    ('4', 'Robotics'),
    ('9', 'Quizzing'),
    ('12', 'Departmental Events'),
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
    fees = models.IntegerField(default = 400)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    prize = models.IntegerField()
    rulebook = models.URLField()
    start_date_time = models.DateTimeField(blank=False)
    end_date_time = models.DateTimeField(blank=False)

    def __str__(self):
        return self.name+"\t"+self.coordinator.name


class Participant(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, blank=False, default = 'Your Name')
    phone_number = models.CharField(max_length=10, default=None)
    college_name = models.CharField(max_length=200, default='no college')
    ca_code = models.ForeignKey(Profile , verbose_name = 'CA Code', null = True, blank= True, on_delete = models.CASCADE)
    participant_code = models.CharField(
        max_length=11, verbose_name='Participant Code', unique=True)
    
    def __str__(self):
        return self.user.username+"\t"+self.college_name

class Payment(models.Model):

    participant = models.OneToOneField(Participant, on_delete = models.CASCADE, primary_key = True)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.participant.__str__()

class EventRegistration(models.Model):

    event = models.ForeignKey(Events, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)

    def __str__(self):
        return self.participant.__str__()+"\t"+self.event.__str__()

class Team(models.Model):

    name = models.CharField(max_length = 100, verbose_name = 'Team Name')
    leader = models.ForeignKey(Participant, on_delete = models.CASCADE)
    event = models.ForeignKey(Events, on_delete = models.CASCADE)

    def __str__(self):
        return self.name+"\t"+self.leader.__str__()

class TeamHasMembers(models.Model):

    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)

    def __str__(self):
        return self.team.__str__()