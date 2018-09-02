from django.urls import path
from card_manager import views

app_name = 'card_manager'

urlpatterns = [
    path('', views.card_choice, name='card_choice'),
    path('card_register/', views.card_register, name='card_register'),
    path('pool/', views.card_pool, name='card_pool'),
    path('decks/', views.deck_list, name='deck_list'),
    path('proxy/', views.ProxyView.as_view(), name='proxy'),
]
