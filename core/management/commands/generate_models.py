from django.core.management.base import BaseCommand
from django.db import models
from core.models import Entity, Field, Relation
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate Django models from metadata'

    def handle(self, *args, **kwargs):
        # مسیر فایل خروجی
        output_dir = Path('core') / 'generated_models.py'
        output = "from django.db import models\n\n"

        # خواندن موجودیت‌ها
        entities = Entity.objects.all()

        for entity in entities:
            # شروع تعریف کلاس
            output += f"class {entity.name}(models.Model):\n"

            # اضافه کردن فیلدها
            fields = Field.objects.filter(entity=entity)
            for field in fields:
                field_type = {
                    'char': f"CharField(max_length={field.max_length or 255})",
                    'text': "TextField()",
                    'int': "IntegerField()",
                    'float': "FloatField()",
                    'bool': "BooleanField()",
                    'date': "DateField()",
                    'email': "EmailField()",
                }.get(field.field_type, "CharField(max_length=255)")

                # اضافه کردن ویژگی‌های اضافی
                attrs = []
                if field.is_required:
                    attrs.append("blank=False, null=False")
                if field.default_value:
                    attrs.append(f"default='{field.default_value}'")
                if attrs:
                    field_type = field_type.replace(')', f", {', '.join(attrs)})")

                output += f"    {field.name} = models.{field_type}\n"

            # اضافه کردن روابط
            relations = Relation.objects.filter(entity_from=entity)
            for relation in relations:
                relation_type = {
                    'one_to_one': "OneToOneField",
                    'one_to_many': "ForeignKey",
                    'many_to_many': "ManyToManyField",
                }.get(relation.relation_type, "ForeignKey")
                output += f"    {relation.entity_to.name.lower()} = models.{relation_type}('{relation.entity_to.name}', on_delete=models.CASCADE)\n"

            output += "\n"

        # ذخیره فایل
        with open(output_dir, 'w') as f:
            f.write(output)
        self.stdout.write(self.style.SUCCESS(f'Models generated successfully at {output_dir}'))