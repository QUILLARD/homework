from django.contrib import admin
from bboard.models import Bb, Rubric, Parent, Child, Machine, Spare, IceCreamMarket, IceCream


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


admin.site.register(Rubric)
admin.site.register(Bb, BbAdmin)
admin.site.register(Child)
admin.site.register(Parent)
admin.site.register(IceCream)
admin.site.register(IceCreamMarket)
