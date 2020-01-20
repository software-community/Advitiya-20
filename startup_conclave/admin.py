from django.contrib import admin

from startup_conclave.models import (StartupTeam, StartupTeamHasMembers, StartupRegistrations, 
                                        BootCampTeam, BootCampTeamHasMembers, BootCampRegistrations, PaymentForStalls)

class StartupTeamAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupTeam._meta.fields]

admin.site.register(StartupTeam, StartupTeamAdminView)

class StartupTeamHasMembersAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupTeamHasMembers._meta.fields]

admin.site.register(StartupTeamHasMembers, StartupTeamHasMembersAdminView)

class StartupRegistrationsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupRegistrations._meta.fields]

admin.site.register(StartupRegistrations, StartupRegistrationsAdminView)

class BootCampTeamAdminView(admin.ModelAdmin):
    list_display = [field.name for field in BootCampTeam._meta.fields]

admin.site.register(BootCampTeam, BootCampTeamAdminView)

class BootCampTeamHasMembersAdminView(admin.ModelAdmin):
    list_display = [field.name for field in BootCampTeamHasMembers._meta.fields]

admin.site.register(BootCampTeamHasMembers, BootCampTeamHasMembersAdminView)

class BootCampRegistrationsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in BootCampRegistrations._meta.fields]

admin.site.register(BootCampRegistrations, BootCampRegistrationsAdminView)

class PaymentForStallsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in PaymentForStalls._meta.fields]

admin.site.register(PaymentForStalls, PaymentForStallsAdminView)