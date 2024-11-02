from django.contrib import admin
from  .models import *
# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_image', 'location', 'submitted_at','status','manual_status')
    list_filter = ('user', 'submitted_at')
    search_fields = ('location',)
    ordering = ('-submitted_at',)

admin.site.register(Report, ReportAdmin)







