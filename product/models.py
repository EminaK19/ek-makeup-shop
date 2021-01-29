from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_countries.fields import CountryField
from django.db import models
import uuid
from pytils.translit import slugify
from time import time


def gen_slug(s):
    slug = slugify(s)
    return slug + '-' + str(int(time()))


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, primary_key=True, blank=True)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProdusedBy(models.Model):
    uuid = models.UUIDField(primary_key=True, blank=True)
    company = models.CharField(max_length=150)
    country = CountryField(blank_label='(select country)')

    def __str__(self):
        return self.company

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='product_category')
    companies = models.ManyToManyField(ProdusedBy, related_name='product_company')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
            super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)

    def get_avg_rating(self):
        rating_items = self.rating.all()
        values = rating_items.aggregate(avg=Avg('rating'))
        return values['avg']


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, related_name='images',
                                on_delete=models.CASCADE)


class ProductColorImage(models.Model):
    color_image = models.ImageField(upload_to='products_color')
    product = models.ForeignKey(Product, related_name='products_color_image',
                                on_delete=models.CASCADE)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=800)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.author} on {self.product}, created at {self.created_at}'


class Rating (models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return f'Rating of product {self.item} by {self.author} is {self.rating} star(s)'


