# core/forms.py
from django import forms
from .models import Entity, Field, Relation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter entity name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['entity', 'name', 'field_type', 'is_required', 'max_length', 'default_value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter field name'}),
            'field_type': forms.Select(attrs={'class': 'form-control'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max length (optional)'}),
            'default_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Default value (optional)'}),
            'entity': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))

class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = ['entity_from', 'entity_to', 'relation_type']
        widgets = {
            'entity_from': forms.Select(attrs={'class': 'form-control'}),
            'entity_to': forms.Select(attrs={'class': 'form-control'}),
            'relation_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))