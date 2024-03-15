from django.contrib import admin

from .models import *

def delete_selected(modeladmin,request,queryset):
    queryset.delete()
delete_selected.short_description = "Delete selected items"

class PortfolioAdmin(admin.ModelAdmin):
    actions = [delete_selected]

class AboutMeAdmin(admin.ModelAdmin):
    actions = [delete_selected]

class ContactAdmin(admin.ModelAdmin):
        actions = [delete_selected]


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(Contact, ContactAdmin)

