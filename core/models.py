# core/models.py
from django.db import models

class Entity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"

class Field(models.Model):
    FIELD_TYPES = (
        ('char', 'String'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('bool', 'Boolean'),
        ('date', 'Date'),
        ('text', 'Text'),
        ('email', 'Email'),
    )
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=False)
    max_length = models.PositiveIntegerField(null=True, blank=True)
    default_value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.entity.name}.{self.name}"

    class Meta:
        unique_together = ('entity', 'name')
        verbose_name = "Field"
        verbose_name_plural = "Fields"

class Relation(models.Model):
    RELATION_TYPES = (
        ('one_to_one', 'One to One'),
        ('one_to_many', 'One to Many'),
        ('many_to_many', 'Many to Many'),
    )
    entity_from = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='relations_from')
    entity_to = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='relations_to')
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.entity_from.name} -> {self.entity_to.name} ({self.relation_type})"

    class Meta:
        verbose_name = "Relation"
        verbose_name_plural = "Relations"

# وارد کردن مدل‌های تولید‌شده
try:
    from .generated_models import *
except ImportError:
    pass