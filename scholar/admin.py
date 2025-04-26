from django.contrib import admin
from .models import *
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display =('first_name', 'last_name', 'email', 'role')
admin.site.register(CustomUser, UsersAdmin)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
admin.site.register(StudentProfile, StudentProfileAdmin)

class ScholarShipAdmin(admin.ModelAdmin):
    list_display = ('scholarship_name', 'deadline')
admin.site.register(Scholarship, ScholarShipAdmin)

class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('scholarship', 'student', 'application_date')
admin.site.register(ScholarshipApplication, ScholarshipApplicationAdmin)