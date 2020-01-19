from django.db import models
from main_page.models import Participant
import os

class StartupTeam(models.Model):

    name = models.CharField(max_length = 100, verbose_name = 'Team Name')
    leader = models.ForeignKey(Participant, on_delete = models.CASCADE)

    def __str__(self):
        return self.name+"\t"+self.leader.__str__()

class StartupTeamHasMembers(models.Model):

    team = models.ForeignKey(StartupTeam, on_delete = models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)

    def __str__(self):
        return self.team.__str__()

class StartupRegistrations(models.Model):
    
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.participant.__str__()
    
