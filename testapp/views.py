from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from testapp.forms import SMSCreateForm
from testapp.models import SMS


class AddSms(CreateView):
    template_name = 'testapp/create.html'
    form_class = SMSCreateForm
    success_url = reverse_lazy('index')


class ReadSms(DetailView):
    model = SMS
    template_name = 'testapp/read.html'


class ReadAllSms(ListView):
    model = SMS
    context_object_name = 'sms'
    template_name = 'testapp/readallsms.html'


class DeleteSms(DeleteView):
    model = SMS
    template_name = 'testapp/deletesms.html'
    context_object_name = 'sms'
    success_url = reverse_lazy('index')


class UpdateSms(UpdateView):
    model = SMS
    template_name = 'testapp/updatesms.html'
    fields = '__all__'
    success_url = reverse_lazy('index')

