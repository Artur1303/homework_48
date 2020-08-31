from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum

DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Продукты питания'),
    ('household', 'Хоз. товары'),
    ('toys', 'Детские игрушки'),
    ('appliances', 'Бытовая Техника')
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, verbose_name='Категория',
                                choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY)
    amount = models.IntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    products = models.ForeignKey('webapp.Product', related_name='baskets',on_delete=models.DO_NOTHING, verbose_name='Карзина')
    qty = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(0)])

    def total(self):
        return self.products.price * self.qty


class Orders(models.Model):
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    adress =  models.CharField(max_length=100, verbose_name='Адресс')
    created_at =models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')


class ProductOrder(models.Model):
    order=models.ForeignKey('webapp.Orders', verbose_name='Номер заказа', related_name='ProductOrders', on_delete=models.CASCADE)
    product =models.ForeignKey('webapp.Product', verbose_name='Номер заказа', related_name='OrderProducts', on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(0), ])