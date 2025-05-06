# core/views.py
from django.shortcuts import render, redirect
from .models import Entity
from .forms import EntityForm, FieldForm, RelationForm


def entity_list(request):
    entities = Entity.objects.all()
    return render(request, 'core/entity_list.html', {'entities': entities})


def entity_create(request):
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entity_list')
    else:
        form = EntityForm()
    return render(request, 'core/entity_form.html', {'form': form, 'title': 'Create Entity'})


def field_create(request):
    entity_id = request.GET.get('entity')
    initial = {}
    if entity_id:
        initial['entity'] = Entity.objects.get(id=entity_id)

    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entity_list')
    else:
        form = FieldForm(initial=initial)
    return render(request, 'core/field_form.html', {'form': form, 'title': 'Create Field'})


def relation_create(request):
    entity_id = request.GET.get('entity')
    initial = {}
    if entity_id:
        initial['entity_from'] = Entity.objects.get(id=entity_id)

    if request.method == 'POST':
        form = RelationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entity_list')
    else:
        form = RelationForm(initial=initial)
    return render(request, 'core/relation_form.html', {'form': form, 'title': 'Create Relation'})