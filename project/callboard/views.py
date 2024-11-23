from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse
from .models import Ad, Response


# Объявления (Ad)
class AdList(ListView):
    model = Ad
    template_name = 'callboard/ads.html'
    context_object_name = 'ads'
    paginate_by = 10  # Пагинация


class AdDetail(DetailView):
    model = Ad
    template_name = 'callboard/ad_detail.html'
    context_object_name = 'ad'


class AdCreate(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['title', 'content', 'category']
    template_name = 'callboard/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, UpdateView):
    model = Ad
    fields = ['title', 'content', 'category']
    template_name = 'callboard/ad_form.html'
    success_url = reverse_lazy('ad_list')


class AdDelete(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'callboard/ad_confirm_delete.html'
    success_url = reverse_lazy('ad_list')


# Отклики (Response)
class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'callboard/response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(ad__author=self.request.user)


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'callboard/response_detail.html'
    context_object_name = 'response'


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['content', 'ad']
    template_name = 'callboard/response_form.html'
    success_url = reverse_lazy('response_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'callboard/response_confirm_delete.html'
    success_url = reverse_lazy('response_list')


class ResponseAccept(LoginRequiredMixin, FormView):
    model = Response
    template_name = 'callboard/response_accept.html'
    success_url = reverse_lazy('response_list')

    def post(self, request, *args, **kwargs):
        response = Response.objects.get(pk=kwargs['pk'])
        response.is_accepted = True
        response.save()
        return super().form_valid(self.get_form())


@login_required
def user_profile(request):
    is_author = request.user.groups.filter(name='authors').exists()
    return render(request, 'account/user_profile.html', {
        'is_author': is_author,
    })