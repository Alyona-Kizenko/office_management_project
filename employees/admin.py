from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "position", "workplace"]
    list_filter = ["position", "workplace"]
    search_fields = ["first_name", "last_name", "email"]
