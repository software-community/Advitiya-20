from django import forms

from accomodation.models import Meal, AccommodationDetail


class MealForm(forms.ModelForm):
    MEAL_CHOICE = (
        ("b", "Breakfast"),
        ("l", "Lunch"),
        ("d", "Dinner"),
    )
    meal_on_7th = forms.MultipleChoiceField(choices=MEAL_CHOICE, required=False,
        widget=forms.CheckboxSelectMultiple)
    meal_on_8th = forms.MultipleChoiceField(choices=MEAL_CHOICE, required=False,
        widget=forms.CheckboxSelectMultiple)
    meal_on_9th = forms.MultipleChoiceField(choices=MEAL_CHOICE, required=False,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Meal
        fields = ['meal_on_7th', 'meal_on_8th', 'meal_on_9th']

    def clean_meal_on_7th(self):
        meal = self.cleaned_data['meal_on_7th']
        meal = ''.join(meal)
        return meal

    def clean_meal_on_8th(self):
        meal = self.cleaned_data['meal_on_8th']
        meal = ''.join(meal)
        return meal

    def clean_meal_on_9th(self):
        meal = self.cleaned_data['meal_on_9th']
        meal = ''.join(meal)
        return meal

class AccommodationDetailForm(forms.ModelForm):

    class Meta:
        model = AccommodationDetail
        fields = ['accomodation_on_7th', 'accomodation_on_8th', 'accomodation_on_9th']