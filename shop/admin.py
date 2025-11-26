from django.contrib import admin
from .models import Category, Product, Image, Attribute, AttributeKey, AttributeValue
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html


admin.site.register(Product)
admin.site.register(Image)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'slug']
    prepopulated_fields = {"slug": ("title",)}

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;"/>',
                obj.image.url
            )
        return "-"
    
    image_preview.short_description = "Image"


admin.site.register(Attribute)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)


# Register your models here.
