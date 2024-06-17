from django.contrib import admin
from .models import category,product,ProductImage,SizeVariant,ColorVariant,Coupon
admin.site.register(category)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price']
    inlines = [ProductImageAdmin]
admin.site.register(product,ProductAdmin)
admin.site.register(ProductImage)
@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name','price']
    model = SizeVariant


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name','price']
    model = ColorVariant



admin.site.register(Coupon)


# admin.site.register(SizeVariant)


# Register your models here.
