from django.contrib import admin
from bboard.models import Bb, Rubric


class BbAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'price', 'time_create', 'rubric')
    list_display_links = ('id', 'title', 'content')
    search_fields = ('title', 'content')
    readonly_fields = ('time_create', 'time_update')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('time_create', 'rubric',)


class RubricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Rubric, RubricAdmin)
admin.site.register(Bb, BbAdmin)
