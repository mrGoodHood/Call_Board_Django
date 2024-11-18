from django.urls import path
from . import views

urlpatterns = [
    # Маршруты для работы с объявлениями (Ad)
    path('ads/', views.AdList.as_view(), name='ads'),           # Список объявлений
    path('ads/<int:pk>/', views.AdDetail.as_view(), name='ad_detail'),  # Детали объявления
    path('ads/create/', views.AdCreate.as_view(), name='ad_create'),    # Создание объявления
    path('ads/<int:pk>/update/', views.AdUpdate.as_view(), name='ad_update'),  # Редактирование объявления
    path('ads/<int:pk>/delete/', views.AdDelete.as_view(), name='ad_delete'),  # Удаление объявления

    # Маршруты для работы с откликами (Response)
    path('responses/', views.ResponseList.as_view(), name='response_list'),  # Список откликов
    path('responses/<int:pk>/', views.ResponseDetail.as_view(), name='response_detail'),  # Детали отклика
    path('responses/create/', views.ResponseCreate.as_view(), name='response_create'),    # Создание отклика
    path('responses/<int:pk>/delete/', views.ResponseDelete.as_view(), name='response_delete'),  # Удаление отклика
    path('responses/<int:pk>/accept/', views.ResponseAccept.as_view(), name='response_accept'),  # Принятие отклика
]
