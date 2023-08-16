from django.contrib import admin
from django.utils.safestring import mark_safe

from bboard.models import Bb, Rubric


class BbAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'price', 'get_html_img', 'rubric')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'content')
    readonly_fields = ('time_create', 'time_update', 'get_html_img')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('time_create', 'rubric',)
    fields = ('title', 'slug', 'content', 'price', 'image', 'rubric', 'get_html_img', 'time_create', 'time_update')

    def get_html_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=150>")

    get_html_img.short_description = 'Миниатюра'


class RubricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric, RubricAdmin)
