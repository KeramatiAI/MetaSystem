# core/models.py
from django.db import models

class Entity(models.Model):
    name = models.CharField(max_length=100, unique=True)  # نام موجودیت (مثل User یا Product)
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
    updated_at = models.DateTimeField(auto_now=True)  # زمان به‌روزرسانی

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
    name = models.CharField(max_length=100)  # نام فیلد (مثل username)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)  # نوع داده
    is_required = models.BooleanField(default=False)  # آیا فیلد اجباری است؟
    max_length = models.PositiveIntegerField(null=True, blank=True)  # برای CharField یا TextField
    default_value = models.CharField(max_length=255, null=True, blank=True)  # مقدار پیش‌فرض

    def __str__(self):
        return f"{self.entity.name}.{self.name}"

    class Meta:
        unique_together = ('entity', 'name')  # نام فیلد در هر موجودیت باید یکتا باشد
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entity_from.name} -> {self.entity_to.name} ({self.relation_type})"

    class Meta:
        verbose_name = "Relation"
        verbose_name_plural = "Relations"