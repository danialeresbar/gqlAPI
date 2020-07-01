from django.db import models
from django.contrib.postgres.fields import JSONField


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name='ingredients', on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ('name',)

    def __str__(self):
        return self.name
        

class Dog(models.Model):
    name = models.CharField(max_length=100)
    data = JSONField(blank=True, default=dict)

    class Meta:
        verbose_name = "Perro"
        verbose_name_plural = "Perros"
        ordering = ('id',)

    def __str__(self):
        return self.name
