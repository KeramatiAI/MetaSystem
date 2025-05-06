from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import path, reverse_lazy
from core.generated_models import *
from core.models import Field


class UserListView(ListView):
    model = User
    template_name = 'generated/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [field.name for field in Field.objects.filter(entity__name='User')]
        return context

class UserCreateView(CreateView):
    model = User
    template_name = 'generated/user_form.html'
    fields = '__all__'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    template_name = 'generated/user_form.html'
    fields = '__all__'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'generated/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

class OrderListView(ListView):
    model = Order
    template_name = 'generated/order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [field.name for field in Field.objects.filter(entity__name='Order')]
        return context

class OrderCreateView(CreateView):
    model = Order
    template_name = 'generated/order_form.html'
    fields = '__all__'
    success_url = reverse_lazy('order_list')

class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'generated/order_form.html'
    fields = '__all__'
    success_url = reverse_lazy('order_list')

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'generated/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
