from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.crypto import get_random_string
import os
from ca.models import Profile

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
    phone_number = models.CharField(max_length=10, default=None)
    college_name = models.CharField(max_length=200, default='no college')
    ca_code = models.ForeignKey(Profile , verbose_name = 'CA Code', null = True, blank= True, on_delete = models.CASCADE)
    participant_code = models.CharField(
        max_length=6, verbose_name='Participant Code', unique=True)

    def unique_participant_code(self):
        code = 'ADV_' + get_random_string(length=6).upper()
        while Participant.objects.filter(participant_code = code).exists():
            code = 'ADV_' + get_random_string(length=6).upper()
        return code

    def save(self, *args, **kwargs):
        if not self.participant_code:
            self.participant_code = self.unique_participant_code()

        super().save(*args, **kwargs)

class Payment(models.Model):

    participant = models.OneToOneField(Participant, on_delete = models.CASCADE, primary_key = True)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')

class EventRegistration(models.Model):

    event = models.ForeignKey(Events, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)

class Team(models.Model):

    name = models.CharField(max_length = 100)
    leader = models.ForeignKey(Participant, on_delete = models.CASCADE)
    event = models.ForeignKey(Events, on_delete = models.CASCADE)

class TeamHasMembers(models.Model):

    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)