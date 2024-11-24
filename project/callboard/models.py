from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('tank', 'Танки'),
        ('healer', 'Хилы'),
        ('dd', 'ДД'),
        ('merchant', 'Торговцы'),
        ('guildmaster', 'Гилдмастеры'),
        ('questgiver', 'Квестгиверы'),
        ('blacksmith', 'Кузнецы'),
        ('leatherworker', 'Кожевники'),
        ('alchemist', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Ad(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.author.username})'

    def clean(self):
        valid_categories = [choice[0] for choice in Category.CATEGORY_CHOICES]
        if self.category and self.category.name not in valid_categories:
            raise ValidationError("Выбранная категория недопустима.")
        if not self.content:
            raise ValidationError("Контент объявления не может быть пустым.")

    class Meta:
        permissions = [
            ('can_publish', 'Can publish ads'),  # Пользователь может публиковать объявления
            ('can_mark_urgent', 'Can mark ads as urgent'),  # Пользователь может отмечать объявления как срочные
        ]


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Отклик от {self.author} к "{self.ad.title}"'