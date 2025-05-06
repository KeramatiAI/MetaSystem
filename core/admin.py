from django.contrib import admin
from .models import Entity, Field, Relation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class BaseAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.helper = FormHelper()
        form.helper.layout = Layout(
            *form.base_fields.keys(),
            Submit('submit', 'Save', css_class='btn btn-primary')
        )
        return form

@admin.register(Entity)
class EntityAdmin(BaseAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Field)
class FieldAdmin(BaseAdmin):
    list_display = ('entity', 'name', 'field_type', 'is_required')
    list_filter = ('entity', 'field_type', 'is_required')
    search_fields = ('name',)

@admin.register(Relation)
class RelationAdmin(BaseAdmin):
    list_display = ('entity_from', 'entity_to', 'relation_type', 'created_at')
    list_filter = ('relation_type',)