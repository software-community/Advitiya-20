from django.contrib import admin
from main_page.models import Events, Coordinator, Participant, Payment, EventRegistration, Team, TeamHasMembers

admin.site.register(Events)
admin.site.register(Coordinator)
admin.site.register(Participant)
admin.site.register(Payment)
admin.site.register(EventRegistration)
admin.site.register(Team)
admin.site.register(TeamHasMembers)