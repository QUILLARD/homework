from django.contrib import admin

from tasksheet.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'notes', 'start', 'is_completed']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['start', 'is_completed']
    list_editable = ['is_completed']


admin.site.register(Task, TaskAdmin)
