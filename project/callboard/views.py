import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from .forms import AdForm, SubscriptionForm
from .models import Ad, Response, NewsletterSubscription


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
        queryset = Response.objects.filter(ad__author=self.request.user)
        selected_ad = self.request.GET.get('selected_ad')
        if selected_ad:
            queryset = queryset.filter(ad_id=selected_ad)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = Ad.objects.filter(author=self.request.user)
        return context


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

    # Проверка, является ли текущий пользователь автором
    def dispatch(self, request, *args, **kwargs):
        response = self.get_object()
        if response.ad.author != request.user:
            messages.error(request, 'Вы не имеете права удалять этот отклик.')
            return HttpResponseRedirect(reverse_lazy('response_list'))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Отклик успешно удален.')
        return super().delete(request, *args, **kwargs)


class ResponseAccept(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk)
        if response.ad.author != request.user:
            messages.error(request, 'Вы не имеете права принять этот отклик.')
            return HttpResponseRedirect(reverse_lazy('response_list'))

        response.is_accepted = True
        response.save()

        # Отправка уведомления пользователю
        subject = 'Ваш отклик на объявление принят!'
        message = f'Здравствуйте! Ваш отклик на объявление "{response.ad.title}" был принят.'
        from_email = 'noreply@yourdomain.com'
        recipient_list = [response.author.email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, f'Отклик на объявление {response.ad} принят!')
        return HttpResponseRedirect(reverse_lazy('response_detail', args=[pk]))


@login_required
def user_profile(request):
    is_author = request.user.groups.filter(name='authors').exists()
    return render(request, 'account/user_profile.html', {
        'is_author': is_author,
    })


# Представление для подписки
@login_required
def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription, _ = NewsletterSubscription.objects.get_or_create(user=request.user)
            subscription.subscribed = form.cleaned_data['subscribed']
            subscription.save()
            return redirect('newsletter_success')
    else:
        try:
            subscription = NewsletterSubscription.objects.get(user=request.user)
            form = SubscriptionForm(instance=subscription)
        except NewsletterSubscription.DoesNotExist:
            form = SubscriptionForm(initial={'subscribed': False})

    return render(request, 'subscribe_newsletter.html', {'form': form})

def newsletter_success(request):
    return render(request, 'newsletter_success.html')