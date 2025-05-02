from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Result, User,Course, Reminder,CSESkillDevelopmentCourse


admin.site.register(CSESkillDevelopmentCourse)
admin.site.register(Course)
admin.site.register(Reminder)
admin.site.register(Result)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'student_id')}),
    )
