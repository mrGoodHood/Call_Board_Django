import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from .forms import AdForm
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


class AdCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'callboard/ad_form.html'
    success_url = reverse_lazy('ads')
    permission_required = 'callboard.add_ad'  # Право для создания объявлений

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'callboard/ad_form.html'
    success_url = reverse_lazy('ads')
    permission_required = 'callboard.change_ad'  # Право для редактирования объявлений

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj


class AdDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Ad
    template_name = 'callboard/ad_confirm_delete.html'
    success_url = reverse_lazy('ads')
    permission_required = 'callboard.delete_ad'  # Право для удаления объявлений

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj


# Отклики (Response)
class ResponseList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Response
    template_name = 'callboard/response_list.html'
    context_object_name = 'responses'
    permission_required = 'callboard.view_response'  # Право для просмотра откликов

    def get_queryset(self):
        return Response.objects.filter(ad__author=self.request.user)


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'callboard/response_detail.html'
    context_object_name = 'response'


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['content']
    template_name = 'callboard/response_create.html'
    success_url = reverse_lazy('ads')

    def form_valid(self, form):
        form.instance.ad_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

        # Отправка уведомления автору объявления
        ad = form.instance.ad
        ad_author_email = ad.author.email

        if ad_author_email:  # Проверяем, указан ли email у автора
            send_mail(
                subject='Новый отклик на ваше объявление',
                message=(
                    f"Здравствуйте, {ad.author.username}!\n\n"
                    f"Пользователь {self.request.user.username} оставил отклик на ваше объявление \"{ad.title}\".\n\n"
                    f"Содержание отклика:\n{form.instance.content}\n\n"
                    f"Посмотреть отклик можно в системе."
                ),
                from_email= os.getenv('EMAIL_HOST_USER'),
                recipient_list=[ad_author_email],
                fail_silently=False,
            )

        return response


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