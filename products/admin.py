from django.contrib import admin

from products.models import Product, Category, ProductRating, FeaturedGame

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductRating)
admin.site.register(FeaturedGame)





