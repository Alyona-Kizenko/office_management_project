from django.contrib import admin
from .models import Workplace


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ["desk_number", "employee", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["desk_number", "employee__user__first_name", "employee__user__last_name"]
    ordering = ["desk_number"]
    raw_id_fields = ["employee"]