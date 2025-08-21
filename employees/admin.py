from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Employee, Skill, EmployeeSkill


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = "Дополнительная информация"
    filter_horizontal = ["skills"]


class CustomUserAdmin(UserAdmin):
    inlines = [EmployeeInline]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "gender", "get_skills"]
    list_filter = ["gender", "skills"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    inlines = [EmployeeSkillInline]
    
    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = "Навыки"


class SkillAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ["employee", "skill", "level"]
    list_filter = ["skill", "level"]
    search_fields = ["employee__user__first_name", "employee__user__last_name"]


# Перерегистрируем UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(EmployeeSkill, EmployeeSkillAdmin)