from django.urls import path
from .views import (
    AdList, AdDetail, AdCreate, AdUpdate, AdDelete,
    ResponseList, ResponseDetail, ResponseCreate, ResponseDelete, ResponseAccept,
    user_profile, subscribe_newsletter, newsletter_success,
)

urlpatterns = [
    # Маршруты для работы с объявлениями (Ad)
    path('ads/<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
    path('ads/<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),
    path('ads/<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('ads/create/', AdCreate.as_view(), name='ad_create'),
    path('ads/', AdList.as_view(), name='ads'),

    # Маршруты для работы с откликами (Response)
    path('responses/', ResponseList.as_view(), name='response_list'),
    path('responses/<int:pk>/', ResponseDetail.as_view(), name='response_detail'),
    path('responses/create/<int:ad_id>', ResponseCreate.as_view(), name='response_create'),
    path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('responses/<int:pk>/accept/', ResponseAccept.as_view(), name='response_accept'),

    # Маршруты для подписки
    path('subscribe-newsletter/', subscribe_newsletter, name='subscribe_newsletter'),
    path('newsletter-success/', newsletter_success, name='newsletter_success'),

    # Аккаунт
    path('profile/', user_profile, name='user_profile'),
]
