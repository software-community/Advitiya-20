from django.db import models
from main_page.models import Participant
import os

STARTUP_CATEGORY_CHOCIES = (
    ('1', 'Operational'),
    ('2', 'Operational > 1 year'),
    ('3', 'Idea'),
    ('4', 'Concept'),
    ('5', 'Proof of Concept'),
    ('6', 'Pilot'),
)

REQUIREMENT_CHOICES=(
    ('1', 'Investor/Banks'),
    ('2', 'IPR Company'),
    ('3', 'Company Incorporation'),
    ('4', 'Web & App Development Company'),
    ('5', 'Manufacturing Company'),
    ('6', 'Marketing Company'),
)

COMMITMENT=(
    ('1', 'Full Time'),
    ('2', 'Part Time'),
)

class StartupTeam(models.Model):

    name = models.CharField(max_length = 100, verbose_name = 'Team Name')
    leader = models.ForeignKey(Participant, on_delete = models.CASCADE)
    startup_name= models.CharField(max_length = 100, verbose_name = 'Startup Name', default="Startup Name")
    founder_name = models.CharField(max_length = 100, verbose_name = 'Founder Name', null=True, blank=True)
    founder_phone_number = models.CharField(max_length=50, null=True, blank=True,
            verbose_name="Founder Phone Number")
    startup_category = models.CharField(max_length=30, choices=STARTUP_CATEGORY_CHOCIES, default="1",
            verbose_name="Startup Category")
    sector = models.CharField(max_length = 100, verbose_name = 'Sector', null=True, blank=True)
    why_invest = models.TextField(verbose_name="Tell Investor- Why invest in you?", null=True, blank=True)
    requirements = models.CharField(max_length=40, choices=REQUIREMENT_CHOICES, null=True, blank=True, 
            verbose_name="Requirements of your Startup")
    commitment = models.CharField(max_length=30, choices=COMMITMENT, null=True, blank=True, verbose_name="Commitment")

    def __str__(self):
        return self.startup_name+"\t"+self.leader.__str__()

class BootCampTeam(models.Model):

    name = models.CharField(max_length = 100, verbose_name = 'Team Name')
    leader = models.ForeignKey(Participant, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name+"\t"+self.leader.__str__()

class BootCampTeamHasMembers(models.Model):

    team = models.ForeignKey(BootCampTeam, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)

    def __str__(self):
        return self.team.__str__()

class StartupTeamHasMembers(models.Model):

    team = models.ForeignKey(StartupTeam, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)

    def __str__(self):
        return self.team.__str__()

class StartupRegistrations(models.Model):
    
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    startup_name= models.ForeignKey(StartupTeam, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.startup_name.__str__()
    
class BootCampRegistrations(models.Model):
    
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.participant.__str__()

class PaymentForStalls(models.Model):

    participant=models.ForeignKey(Participant, on_delete = models.CASCADE)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.participant.__str__()