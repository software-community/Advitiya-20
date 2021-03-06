from django.db import models
from main_page.models import Participant

# Create your models here.
class Accommodation(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.participant)

    def is_paid(self):
        if (self.transaction_id != 'none' and self.transaction_id != '0'
            and len(self.transaction_id) > 4):
            return True
        else:
            return False

class AccommodationDetail(models.Model):
    accommodation = models.OneToOneField(Accommodation, on_delete = models.CASCADE)
    accomodation_on_7th = models.BooleanField(default=False)
    accomodation_on_8th = models.BooleanField(default=False)
    accomodation_on_9th = models.BooleanField(default=False)

    def detail(self):
        accs = ''
        if self.accomodation_on_7th:
            accs = accs + '7th '
        if self.accomodation_on_8th:
            accs = accs + '8th '
        if self.accomodation_on_9th:
            accs = accs + '9th '
        return accs

class Meal(models.Model):
    participant = models.OneToOneField(Participant, on_delete = models.CASCADE)
    meal_on_7th = models.CharField(max_length = 3, default = 'none')
    meal_on_8th = models.CharField(max_length = 3, default = 'none')
    meal_on_9th = models.CharField(max_length = 3, default = 'none')

    def detail(self):
        meals = ''
        if self.meal_on_7th:
            meals = meals + self.meal_on_7th + ' on 7th '
        if self.meal_on_8th:
            meals = meals + self.meal_on_8th + ' on 8th '
        if self.meal_on_9th:
            meals = meals + self.meal_on_9th + ' on 9th '
        return meals