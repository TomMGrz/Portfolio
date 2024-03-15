from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

def delete_selected(modeladmin, request, queryset):
    queryset.delete()
delete_selected.short_description = "Delete selected items"

def copy_selected_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # Set primary key to None to create a new object
        obj.save()     # Save the new object to the database
copy_selected_objects.short_description = "Copy selected objects"

class CustomerAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    search_fields = ['first_name', 'last_name', 'email']

class ProductAdmin(TranslationAdmin):  # Inherits from TranslationAdmin now
    actions = [delete_selected, copy_selected_objects]
    search_fields = ['name', 'material', 'color']

class OrderAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    search_fields = ['customer__first_name', 'customer__last_name', 'order_id']

class OrderItemAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    search_fields = ['order__order_id', 'product__name']

class ShippingAddressAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    search_fields = ['customer__first_name', 'customer__last_name', 'address', 'city', 'country']

class ProductVariantAdmin(TranslationAdmin):
    actions = [delete_selected]
    search_fields = ['name', 'product__name']

class ProductDisplayAdmin(TranslationAdmin):
    actions = [delete_selected]
    search_fields = ['name', 'color']

class CatalogAdmin(TranslationAdmin):
    actions = [delete_selected]
    search_fields = ['product__name']

class InvoiceInfoAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    search_fields = ['firm', 'nip', 'address__address']

class ShippingLevelsAdmin(TranslationAdmin):
    actions = [delete_selected]
    search_fields = ['min_weight', 'max_weight', 'cost']

class CurrenciesAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    search_fields = ['name', 'code']

class CountriesAdmin(TranslationAdmin):
    actions = [delete_selected]
    search_fields = ['name', 'code']

class ReturnRequestAdmin(admin.ModelAdmin):
    actions = [delete_selected]


class ReturnItemAdmin(admin.ModelAdmin):
    actions = [delete_selected]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductDisplay, ProductDisplayAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(InvoiceInfo, InvoiceInfoAdmin)
admin.site.register(ShippingLevels, ShippingLevelsAdmin)
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(ReturnRequest, ReturnRequestAdmin)
admin.site.register(ReturnItem, ReturnItemAdmin)