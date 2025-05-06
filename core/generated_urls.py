from django.urls import path
from core.generated_views import *

urlpatterns = [

    path('user/', UserListView.as_view(), name='user_list'),
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    path('order/', OrderListView.as_view(), name='order_list'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_edit'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
]
