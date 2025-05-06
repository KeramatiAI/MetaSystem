from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.entity_list, name='entity_list'),
    path('entities/create/', views.entity_create, name='entity_create'),
    path('fields/create/', views.field_create, name='field_create'),
    path('relations/create/', views.relation_create, name='relation_create'),
]

try:
    from .generated_urls import urlpatterns as generated_urlpatterns
    urlpatterns += generated_urlpatterns
except ImportError:
    pass