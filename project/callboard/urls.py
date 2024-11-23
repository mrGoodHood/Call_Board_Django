from django.urls import path
from .views import (
    AdList, AdDetail, AdCreate, AdUpdate, AdDelete,
    ResponseList, ResponseDetail, ResponseCreate, ResponseDelete, ResponseAccept,
    user_profile,
)

urlpatterns = [
    # Маршруты для работы с объявлениями (Ad)
    path('', AdList.as_view(), name='ads'),           # Список объявлений
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),  # Детали объявления
    path('ads/create/', AdCreate.as_view(), name='ad_create'),    # Создание объявления
    path('ads/<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),  # Редактирование объявления
    path('ads/<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),  # Удаление объявления

    # Маршруты для работы с откликами (Response)
    path('responses/', ResponseList.as_view(), name='response_list'),  # Список откликов
    path('responses/<int:pk>/', ResponseDetail.as_view(), name='response_detail'),  # Детали отклика
    path('responses/create/', ResponseCreate.as_view(), name='response_create'),    # Создание отклика
    path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),  # Удаление отклика
    path('responses/<int:pk>/accept/', ResponseAccept.as_view(), name='response_accept'),  # Принятие отклика

    # Аккаунт
    path('profile/', user_profile, name='user_profile'),
]
