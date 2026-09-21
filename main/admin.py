from django.contrib import admin
from .models import Category, SubCategory, SubSubCategory, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(SubSubCategory)
class SubSubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "subcategory", "subsubcategory", "price", "stock_quantity")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "color", "skin_tone")
    list_filter = ("category", "subcategory", "color", "skin_tone")
