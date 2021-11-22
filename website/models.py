from django.db import models
from django.urls import reverse


class Paper(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    url = models.SlugField(max_length=270, unique=True)
    content = models.TextField()
    visibility = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('paper_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    url = models.SlugField(max_length=110, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.url})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


