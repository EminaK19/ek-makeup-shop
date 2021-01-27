from django.contrib import admin
from .models import Category, ProdusedBy, Product, ProductImage, ProductColorImage, Rating, Review


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', ) # list or tuple


class ColorImageInline(admin.TabularInline):
    model = ProductColorImage
    extra = 2
    fields = ('color_image', )


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline, ColorImageInline
    ]
    list_display = ('uuid', 'title', 'price')
    list_display_links = ('uuid', 'title')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'rating')
    list_display_links = ('id', 'item')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(ProdusedBy)
admin.site.register(Rating, RatingAdmin)
