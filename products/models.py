from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Platform(models.Model):  # Gaming Platform + Genre
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):  # Game
    name = models.CharField(max_length=100)
    date_of_release = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads', blank=True)
    number_in_stock = models.PositiveIntegerField(default=0)
    # out_of_stock = models.BooleanField(default=False)  # not needed
    category = models.ForeignKey(Platform, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True)
    total_rating = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update(self, *args, **kwargs):
        if self.total_rating:
            try:
                super().update(*args, **kwargs)
            except:
                print("Classes are already cancelled.")
                # Product.objects.update(total_rating=69)   in the views.py of ProductRating

    def average_rating(self):
        # implementation to find average rating
        return ProductRating.objects.filter(product=self).aggregate(Avg('star_rating'))['rating__avg'] or 0

    def decrease_stock(self):
        # needs implementing? in the views, CartView?
        pass

    def increase_stock(self):
        pass

    def __str__(self):
        return f"{self.name}: {self.average_rating()}"


class ProductRating(models.Model):  # for giving feedback/comments
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star_rating = models.PositiveIntegerField(default=0)   # from 1 to 5
    comment_field = models.TextField(default='', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.product.name}"


class FeaturedGame(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"


# class DiscountedGame(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.product.name}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.total}"






