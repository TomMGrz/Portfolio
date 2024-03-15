from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'color', 'material', 'subcategory')

@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    fields = ('name', 'subcategory' )

@register(ProductDisplay)
class ProductDisplayTranslationOptions(TranslationOptions):
    fields = ('name', 'color', 'material', 'subcategory')  # Translate fields as needed

@register(Catalog)
class CatalogTranslationOptions(TranslationOptions):
    fields = ('name', 'description') 

@register(Countries)
class CountriesTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(ShippingLevels)
class ShippingLevelsTranslationOptions(TranslationOptions):
    fields = ('courier_name', )