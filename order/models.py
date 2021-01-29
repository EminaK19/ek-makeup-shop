from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Sum

from product.models import Product

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('in_delivery', 'In delivery'),
    ('finished', 'Finished'),
    ('canceled', 'Canceled')
)
PAYMENT_METHOD = (
    ('visa', 'Visa Card'),
    ('mastercard', 'Master Card'),
    ('paypall', 'PayPall'),
    ('mobile_banking', 'Mobile Banking'),
    ('online_wallet', 'Online Wallet')
)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)


#     что делать с total_price, как высчитать


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='orders', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    comment = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    items = models.ManyToManyField(OrderItem, related_name='orders')
    payment = models.CharField(max_length=25, choices=PAYMENT_METHOD)

    # def get_total_price(self):
    #     print(cost)
    #     total_price = cost.aggregate(sum=Sum('price'))
    #     return total_price['sum']

# как в postman загружать фото
# что со списком товаров в ордере
