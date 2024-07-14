from django.contrib import admin

from products.models import Product, Platform, ProductRating, FeaturedGame

# Register your models here.


admin.site.register(Product)
admin.site.register(Platform)
admin.site.register(ProductRating)
admin.site.register(FeaturedGame)





