from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from .models import Ad, NewsletterSubscription
from ckeditor.widgets import CKEditorWidget
from .models import Response


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category']
        widgets = {
            'content': CKEditorWidget(),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Текст отклика:"


# Форма для подписки
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['subscribed']