from django.contrib import admin

from users.models import User, Applicant, Director, GeneralAffairs, ProjectManager, Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('email','username','name', 'phone', 'password','role','foto','is_active')
    list_display = ('user_id','email','username','name', 'phone','password','role','foto','is_active')

@admin.register(Applicant)
class ApplicantsAdmin(admin.ModelAdmin):
    fields = ("user","application_list","is_accepted")
    list_display = ("applicant_id","user","application_list","is_accepted")

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")

@admin.register(GeneralAffairs)
class GeneralAffairsAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")

@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")
