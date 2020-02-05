from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.crypto import get_random_string
import os
import string
from ca.models import Profile

from django.utils.timezone import make_aware
import datetime

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

class Participant(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, blank=False, default = 'Your Name')
    phone_number = models.CharField(max_length=10, default=None)
    college_name = models.CharField(max_length=200, default='no college')
    city = models.CharField(max_length = 50)
    ca_code = models.ForeignKey(Profile , verbose_name = 'CA Code', null = True, blank= True, on_delete = models.CASCADE)
    participant_code = models.CharField(
        max_length=11, verbose_name='Participant Code', unique=True)
    
    def __str__(self):
        return self.user.username+"\t"+self.college_name + "\t"+ str(self.phone_number)

    def has_participated_in_workshop(self):
        date_time = datetime.datetime(2020, 1, 17)
        participant_registrations = WorkshopRegistration.objects.filter(
            participant=self, timestamp__gte=make_aware(date_time))
        bool_participated = False
        for participant_registration in participant_registrations:
            if participant_registration.is_paid():
                bool_participated = True
                break
        return bool_participated
    
    def has_participated_any_workshop(self):
        participant_registrations = WorkshopRegistration.objects.filter(participant=self)
        bool_participated = False
        for participant_registration in participant_registrations:
            if participant_registration.is_paid():
                bool_participated = True
                break
        return bool_participated
    
    def has_valid_payment(self):
        try:
            payment = Payment.objects.get(participant=self)
            return payment.is_paid()
        except:
            return False

class Coordinator(models.Model):
    name = models.CharField(max_length=100)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name + "\t"+self.phone

class Events(models.Model):

    category = models.CharField(max_length=20, choices=CATEGORY_CHOCIES)
    image = models.ImageField(
        upload_to=get_file_path, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    venue = models.CharField(max_length=100)
    team_lower_limit = models.IntegerField()
    team_upper_limit = models.IntegerField()
    fees = models.IntegerField(default = 400)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    prize = models.DecimalField(max_digits=6, decimal_places=3)
    rulebook = models.URLField()
    start_date_time = models.DateTimeField(blank=False)
    end_date_time = models.DateTimeField(blank=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name+"\t"+self.coordinator.name
    
    @property
    def photo_url(self):
        return self.image.url if self.image else ''

class Payment(models.Model):

    participant = models.OneToOneField(Participant, on_delete = models.CASCADE, primary_key = True)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.participant.__str__()

    def is_paid(self):
        if (self.transaction_id != 'none' and self.transaction_id != '0'
            and len(self.transaction_id) > 4):
            return True
        else:
            return False

class EventRegistration(models.Model):

    event = models.ForeignKey(Events, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

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

class Workshop(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to=get_file_path, null=True, blank=True)
    fees = models.IntegerField(default = 1000)
    rulebook = models.URLField(blank=True)
    at_sudhir = models.BooleanField(default=False)
    show = models.BooleanField(default=True)

    WORKSHOP_CHOCIES = (
        ('t', 'Technical'),
        ('m', 'Management'),
        ('c', 'Career Training'),
    )
    workshop_type = models.CharField(max_length=2, choices=WORKSHOP_CHOCIES)

    def __str__(self):
        return self.name.__str__()

    @property
    def photo_url(self):
        return self.image.url if self.image else ''

class WorkshopRegistration(models.Model):
    
    workshop = models.ForeignKey(Workshop, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.participant.__str__()+"\t"+self.workshop.__str__()

    def is_paid(self):
        if self.transaction_id != 'none' and self.transaction_id != '0':
            return True
        else:
            return False

class WorkshopAccomodation(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    accomodation_on_7th = models.BooleanField(default=False)
    accomodation_on_8th = models.BooleanField(default=False)
    accomodation_on_9th = models.BooleanField(default=False)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now=True)

    def is_paid(self):
        if (self.transaction_id != 'none' and self.transaction_id != '0'
            and len(self.transaction_id) > 4):
            return True
        else:
            return False

    def no_of_days(self):
        days = 0
        if self.accomodation_on_7th == True:
            days= days+1
        if self.accomodation_on_8th == True:
            days= days+1
        if self.accomodation_on_9th == True:
            days= days+1
        return days

def get_file_path_talk(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.name + '.' + ext
    foldername = 'talk'
    return os.path.join(foldername, filename)

class Talk(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to=get_file_path_talk, null=True, blank=True)
    venue = models.CharField(max_length=100)
    start_date_time = models.DateTimeField(blank=False)
    para1 = models.TextField(null=True, blank=True)
    para2 = models.TextField(null=True, blank=True)
    para3 = models.TextField(null=True, blank=True)
    para4 = models.TextField(null=True, blank=True)
    show = models.BooleanField(default=True)
    link = models.CharField(max_length=150, default="Google_Form_Link")
    show_link = models.BooleanField(default=False)

    @property
    def photo_url(self):
        return self.image.url if self.image else ''

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
# Triggers when a worshop is deleted. Adds to WorkshopHadArtist
@receiver(pre_delete, sender=WorkshopRegistration, dispatch_uid='workshop_delete_signal')
def log_deleted_workshop(sender, instance, using, **kwargs):
    send_mail(subject='Workshop Deleted',
        message='',
        from_email=os.environ.get('EMAIL_HOST_USER', ''),
        recipient_list=['2017csb1073@iitrpr.ac.in', '2017csb1064@iitrpr.ac.in'],
        fail_silently=True,
        html_message= str(instance.workshop) + '\t' + str(instance.participant) +
            '\t' + str(instance.payment_request_id) + '\t' + str(instance.transaction_id)
    )

@receiver(pre_delete, sender=Payment, dispatch_uid='payment_delete_signal')
def log_deleted_payment(sender, instance, using, **kwargs):
    send_mail(subject='Payment Deleted',
        message='',
        from_email=os.environ.get('EMAIL_HOST_USER', ''),
        recipient_list=['2017csb1073@iitrpr.ac.in', '2017csb1064@iitrpr.ac.in'],
        fail_silently=True,
        html_message= str(instance.participant) +
            '\t' + str(instance.payment_request_id) + '\t' + str(instance.transaction_id)
    )
    
@receiver(pre_delete, sender=EventRegistration, dispatch_uid='EventRegistration_delete_signal')
def log_deleted_EventRegistration(sender, instance, using, **kwargs):
    send_mail(subject='EventRegistration Deleted',
        message='',
        from_email=os.environ.get('EMAIL_HOST_USER', ''),
        recipient_list=['2017csb1073@iitrpr.ac.in', '2017csb1064@iitrpr.ac.in'],
        fail_silently=True,
        html_message= str(instance.event) + '\t' + str(instance.participant)
    )