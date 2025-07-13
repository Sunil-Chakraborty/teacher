from django.contrib import admin
from .models import ProductMaster

@admin.register(ProductMaster)
class ProductMasterAdmin(admin.ModelAdmin):
    list_display = ("product_code", "product_name", "belt_type", "tensile_strength", "width_mm", "unit_price", "is_active")
    search_fields = ("product_code", "product_name", "tensile_strength")
    list_filter = ("belt_type", "cover_grade", "is_active")
