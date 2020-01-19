from django.contrib import admin

from startup_conclave.models import StartupTeam, StartupTeamHasMembers, StartupRegistrations, BootCampRegistrations

class StartupTeamAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupTeam._meta.fields]

admin.site.register(StartupTeam, StartupTeamAdminView)

class StartupTeamHasMembersAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupTeamHasMembers._meta.fields]

admin.site.register(StartupTeamHasMembers, StartupTeamHasMembersAdminView)

class StartupRegistrationsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in StartupRegistrations._meta.fields]

admin.site.register(StartupRegistrations, StartupRegistrationsAdminView)

class BootCampRegistrationsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in BootCampRegistrations._meta.fields]

admin.site.register(BootCampRegistrations, BootCampRegistrationsAdminView)