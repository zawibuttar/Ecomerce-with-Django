from django.contrib import admin
from .models import category,product,ProductImage
admin.site.register(category)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
admin.site.register(product,ProductAdmin)
admin.site.register(ProductImage)

# Register your models here.
