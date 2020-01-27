from django.contrib import admin

from startup_conclave.models import (StartupTeam, StartupTeamHasMembers, StartupRegistrations,
        RequirementChoices, StartupTeamHasRequirements, BootCampTeam, BootCampTeamHasMembers,
        BootCampRegistrations, PayForStalls, RegisterForStalls, RegisterForStallsHasMembers)

class StartupTeamAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupTeam._meta.fields]
    list_display.append('requirement_names')

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

class PayForStallsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in PayForStalls._meta.fields]

admin.site.register(PayForStalls, PayForStallsAdminView)

class RegisterForStallsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in RegisterForStalls._meta.fields]

admin.site.register(RegisterForStalls, RegisterForStallsAdminView)

class RequirementChoicesAdminView(admin.ModelAdmin):
    list_display = [field.name for field in RequirementChoices._meta.fields]

admin.site.register(RequirementChoices, RequirementChoicesAdminView)

class StartupTeamHasRequirementsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupTeamHasRequirements._meta.fields]

admin.site.register(StartupTeamHasRequirements, StartupTeamHasRequirementsAdminView)

class RegisterForStallsHasMembersAdminView(admin.ModelAdmin):
    list_display = [field.name for field in RegisterForStallsHasMembers._meta.fields]

admin.site.register(RegisterForStallsHasMembers, RegisterForStallsHasMembersAdminView)