from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify


class Platform(models.Model):  # Gaming Platform
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Platform, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Genre(models.Model):  # game genre
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class AgeRating(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):  # Game
    name = models.CharField(max_length=100)
    date_of_release = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='', blank=True)
    number_in_stock = models.PositiveIntegerField(default=0)
    platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING)
    genre = models.ManyToManyField(Genre)
    age_rating = models.ForeignKey(AgeRating, on_delete=models.DO_NOTHING)
    description = models.TextField(default='', blank=True)
    total_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def average_rating(self):
        ratings = ProductRating.objects.filter(product=self)
        if ratings.exists():
            average_rating = ratings.aggregate(Avg('star_rating'))['star_rating__avg']
            self.total_rating = average_rating
            self.save()
            return average_rating
        return 0

    def __str__(self):
        return f"{self.name} (rating: {self.total_rating})"  # average_rating


class ProductRating(models.Model):  # for giving feedback/comments
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    star_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])   # from 1 to 5
    feedback = models.TextField(default='', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user}: {self.product.name} - {self.star_rating} stars"


class FeaturedGame(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        total_sum = CartItem.objects.all()
        return total_sum

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ordered_items = models.ManyToManyField(Product, through='OrderItem')
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    order_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: order_id: {self.id}"


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"




