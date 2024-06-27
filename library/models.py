from django.db import models

# Create your models here.

class Books(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    count_page = models.PositiveIntegerField(verbose_name='Количество страниц')
    price = models.FloatField(verbose_name='Цена')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата издания')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата написания')
    update_date = models.DateField(auto_now=True, verbose_name='Дата последнего обновления')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Обложка')
    exists = models.BooleanField(default=True, verbose_name='Выпущена?')

    publisher = models.ForeignKey("Publishing_house", on_delete=models.PROTECT, null=True, verbose_name='Издательство')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['name', '-price']

class Publishing_house(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    agent_name = models.CharField(max_length=50, verbose_name='Имя представителя')
    agent_last_name = models.CharField(max_length=50, verbose_name='Фамилия представилеля')
    agent_surname = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    telephone = models.CharField(max_length=20, verbose_name='Номер телефона')

    def __str__(self):
        return self.title + " (" + self.agent_name + " " + self.agent_last_name + ") | " + self.telephone

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

        permissions = [
            ('change_only_telephone', 'Может только добавлять телефон')
        ]

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=255, verbose_name='Описание')
    books = models.ManyToManyField(Books)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Passport_book(models.Model):
    article = models.IntegerField(verbose_name='Артикль')
    features = models.CharField(max_length=255,null=True, blank=True, verbose_name='Дополнение')

    book = models.OneToOneField(Books, on_delete=models.PROTECT, primary_key=True, verbose_name='Книга')

    def __str__(self):
        return str(self.article) + " | " + self.book.__str__()

    class Meta:
        verbose_name = 'Паспорт книги'
        verbose_name_plural = 'Паспорта книг'