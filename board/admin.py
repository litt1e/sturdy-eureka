from django.contrib import admin
from board.models import Section, Thread, Part, Answer

# Register your models here.


class SectionAdmin(admin.ModelAdmin):
        list_display = ('title')


class PartAdmin(admin.ModelAdmin):
        list_display = ('title', 'section', 'short_title')


class ThreadAdmin(admin.ModelAdmin):
        list_display = ('title', 'text', 'date', 'part', )
        list_filter = ('date',)
        date_hierarchy = 'date'
        ordering = ('-date',)


class AnswerAdmin(admin.ModelAdmin):
        list_display = ('text', 'date', 'thread')



admin.site.register(Section)
admin.site.register(Part, PartAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Answer, AnswerAdmin)
