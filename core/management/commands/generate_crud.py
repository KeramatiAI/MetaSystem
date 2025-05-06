from django.core.management.base import BaseCommand
from pathlib import Path
import os
from core.models import Entity, Field

class Command(BaseCommand):
    help = 'Generate CRUD views, URLs, and templates for generated models'

    def handle(self, *args, **kwargs):
        # مسیرهای خروجی
        views_path = Path('core') / 'generated_views.py'
        urls_path = Path('core') / 'generated_urls.py'
        templates_dir = Path('templates') / 'generated'
        templates_dir.mkdir(parents=True, exist_ok=True)

        # تولید محتوای فایل views
        views_content = """from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import path, reverse_lazy
from core.generated_models import *
from core.models import Field

"""
        urls_content = """from django.urls import path
from core.generated_views import *

urlpatterns = [
"""
        entities = Entity.objects.all()

        if not entities.exists():
            self.stdout.write(self.style.WARNING('No entities found in the database. Please add entities first.'))
            return

        for entity in entities:
            model_name = entity.name
            lower_model_name = model_name.lower()

            # تولید ویوها
            views_content += f"""
class {model_name}ListView(ListView):
    model = {model_name}
    template_name = 'generated/{lower_model_name}_list.html'
    context_object_name = '{lower_model_name}s'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [field.name for field in Field.objects.filter(entity__name='{model_name}')]
        context['fields'] = fields
        object_list = context['{lower_model_name}s']
        context['object_field_values'] = [
            {{'object': obj, 'values': [getattr(obj, field) if getattr(obj, field, None) is not None else 'N/A' for field in fields]}}
            for obj in object_list
        ]
        return context

class {model_name}CreateView(CreateView):
    model = {model_name}
    template_name = 'generated/{lower_model_name}_form.html'
    fields = '__all__'
    success_url = reverse_lazy('{lower_model_name}_list')

class {model_name}UpdateView(UpdateView):
    model = {model_name}
    template_name = 'generated/{lower_model_name}_form.html'
    fields = '__all__'
    success_url = reverse_lazy('{lower_model_name}_list')

class {model_name}DeleteView(DeleteView):
    model = {model_name}
    template_name = 'generated/{lower_model_name}_confirm_delete.html'
    success_url = reverse_lazy('{lower_model_name}_list')
"""

            # تولید URLها
            urls_content += f"""
    path('{lower_model_name}/', {model_name}ListView.as_view(), name='{lower_model_name}_list'),
    path('{lower_model_name}/create/', {model_name}CreateView.as_view(), name='{lower_model_name}_create'),
    path('{lower_model_name}/<int:pk>/edit/', {model_name}UpdateView.as_view(), name='{lower_model_name}_edit'),
    path('{lower_model_name}/<int:pk>/delete/', {model_name}DeleteView.as_view(), name='{lower_model_name}_delete'),
"""

            # تولید قالب‌ها
            list_template = """{% extends 'base.html' %}
{% block title %}""" + model_name + """ List{% endblock %}
{% block content %}
<h2>""" + model_name + """ List</h2>
<a href="{% url '""" + lower_model_name + """_create' %}" class="btn btn-primary mb-3">Create New """ + model_name + """</a>
<table class="table">
    <thead>
        <tr>
            {% for field in fields %}
            <th>{{ field|title }}</th>
            {% endfor %}
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for item in object_field_values %}
        <tr>
            {% for value in item.values %}
            <td>{{ value }}</td>
            {% endfor %}
            <td>
                <a href="{% url '""" + lower_model_name + """_edit' item.object.pk %}" class="btn btn-sm btn-warning">Edit</a>
                <a href="{% url '""" + lower_model_name + """_delete' item.object.pk %}" class="btn btn-sm btn-danger">Delete</a>
            </td>
        </tr>
        {% empty %}
        <tr><td colspan="{{ fields|length|add:1 }}" class="text-center">No """ + model_name + """s available</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
"""
            form_template = """{% extends 'base.html' %}
{% block title %}{% if form.instance.pk %}Edit """ + model_name + """{% else %}Create """ + model_name + """{% endif %}{% endblock %}
{% block content %}
<h2>{% if form.instance.pk %}Edit """ + model_name + """{% else %}Create """ + model_name + """{% endif %}</h2>
<form method="post">
    {% csrf_token %}
    {% load crispy_forms_tags %}
    {% crispy form %}
    <button type="submit" class="btn btn-primary">Save</button>
    <a href="{% url '""" + lower_model_name + """_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
"""
            delete_template = """{% extends 'base.html' %}
{% block title %}Delete """ + model_name + """{% endblock %}
{% block content %}
<h2>Delete """ + model_name + """</h2>
<p>Are you sure you want to delete "{{ object }}"?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Confirm Delete</button>
    <a href="{% url '""" + lower_model_name + """_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
"""

            # ذخیره قالب‌ها
            with open(templates_dir / f'{lower_model_name}_list.html', 'w', encoding='utf-8') as f:
                f.write(list_template)
            with open(templates_dir / f'{lower_model_name}_form.html', 'w', encoding='utf-8') as f:
                f.write(form_template)
            with open(templates_dir / f'{lower_model_name}_confirm_delete.html', 'w', encoding='utf-8') as f:
                f.write(delete_template)

        urls_content += "]\n"

        # ذخیره فایل‌های views و urls
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(views_content)
        with open(urls_path, 'w', encoding='utf-8') as f:
            f.write(urls_content)

        self.stdout.write(self.style.SUCCESS(
            f'CRUD views, URLs, and templates generated successfully at:\n'
            f'- Views: {views_path}\n'
            f'- URLs: {urls_path}\n'
            f'- Templates: {templates_dir}'
        ))