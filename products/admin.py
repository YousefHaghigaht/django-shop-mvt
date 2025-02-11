from django.contrib import admin
from .models import Category,Product

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','is_available')
    list_filter = ('is_available',)
    raw_id_fields = ('category',)

