from django.db import models

# Create your models here.
MAX_LENGTH_CHAR = 255

class Supplier(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название')
    agent_firstname = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Фамилия представителя')
    agent_name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Имя представителя')
    agent_surname = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Отчество представителя')
    agent_telephone = models.CharField(max_length=16, verbose_name='Телефон представителя')
    address = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Адрес')
    is_exists = models.BooleanField(default=True, verbose_name='Логическое удаление')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

class Supply(models.Model):
    date_supply = models.DateTimeField(verbose_name='Дата поставки')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='Поставщик')

    product = models.ManyToManyField('Product', through='Pos_supply', verbose_name='Продукты')

    def __str__(self):
        return f'#{self.pk} - {self.date_supply} {self.supplier.name}'

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

class Parametr(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название')
    description = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название')
    description = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Order(models.Model):
    SHOP = "SH"
    COURIER = "CR"
    PICKUPPOINT = "PP"
    TYPE_DELIVERY = [
        (SHOP, 'Вывоз из магазина'),
        (COURIER, 'Курьер'),
        (PICKUPPOINT, 'Пункт выдачи заказов'),
    ]

    buyer_firstname = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Фамилия покупателя')
    buyer_name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Имя покупателя')
    buyer_surname = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Отчество покупателя')
    comment = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Комментарий к заказу')
    delivery_address = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Адрес доставки')
    delivery_type = models.CharField(max_length=2, choices=TYPE_DELIVERY, default=SHOP, verbose_name='Способ доставки')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения заказа')

    product = models.ManyToManyField('Product', through='Pos_order', verbose_name='Товар')
    def __str__(self):
        return f'#{self.pk} - {self.buyer_firstname} {self.buyer_name} ({self.date_create})'


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название')
    description = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    date_create = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True,verbose_name='Фотография товара')
    is_exists = models.BooleanField(default=True, verbose_name='Логическое удаление')

    warehouse = models.ManyToManyField('Warehouse', through='Inventory', verbose_name='Склад')
    parametr = models.ManyToManyField(Parametr, through='Pos_parametr', verbose_name='Характеристики')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    tag = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='Тег')

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Pos_parametr(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    parametr = models.ForeignKey(Parametr, on_delete=models.PROTECT, verbose_name='Характеристика')
    value = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Значение')

    def __str__(self):
        return f'{self.product.name} - {self.parametr.name} ({self.value})'

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'

class Pos_order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество продукта')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка на позицию')

    def __str__(self):
        return f'{self.order.pk} {self.product.name} ({self.order.buyer_firstname} {self.order.buyer_name})'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

class Pos_supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    supply = models.ForeignKey(Supply, on_delete=models.PROTECT, verbose_name='Поставка')
    count = models.PositiveIntegerField(verbose_name='Количество товара')

    def __str__(self):
        return f'{self.product.name} ({self.count}) - #{self.supply.pk}'

    class Meta:
        verbose_name = 'Позиция поставки'
        verbose_name_plural = 'Позиции поставок'

class Warehouse(models.Model):
    AIRPLANE = "AR"
    TRAIN = "TR"
    TRUCK = "TC"
    ALL = "AL"
    TYPE_POST = [
        (AIRPLANE, 'Отправка самолетом'),
        (TRAIN, 'Отправка поездом'),
        (TRUCK, 'Отправка фурой'),
        (ALL, 'Любой тип отправки'),
    ]
    owner_firstname = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Фамилия владельца')
    owner_name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Имя владельца')
    owner_surname = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Отчество владельца')
    location = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Расположение')
    type_post = models.CharField(max_length=2, choices=TYPE_POST, default=ALL, verbose_name='Способ отправки')
    capacity = models.PositiveIntegerField(default=10000, verbose_name='Вместимость')

    def __str__(self):
        return f'{self.location} ({self.capacity} ячеек)'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='Склад')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    single_item = models.FloatField(verbose_name='Вес одной позиции')

    def __str__(self):
        return f'{self.product.name} хранится на №{self.warehouse.pk} ({self.quantity})'

    class Meta:
        verbose_name = 'Хранение позиции'
        verbose_name_plural = 'Хранение позиций'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user_name = models.CharField(max_length=MAX_LENGTH_CHAR, default='anonim', verbose_name='Никнейм пользователя')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг')
    comment = models.TextField(max_length=MAX_LENGTH_CHAR, blank=True, null=True, verbose_name='Комментарий')
    photo = models.ImageField(upload_to='image/review/%Y/%m/%d', blank=True, null=True, verbose_name='Фотография товара')

    def __str__(self):
        return f'{self.product.name} - {self.user_name} ({self.rating})'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

