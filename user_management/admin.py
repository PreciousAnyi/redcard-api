from django.contrib import admin
from .models import User, Student, Invigilator

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Customize admin view if needed
    pass
admin.site.register(Student)
admin.site.register(Invigilator)