from django.urls import path
from card_manager import views

app_name = 'card_manager'

urlpatterns = [
    path('', views.card_choice, name='card_choice'),
    path('card_register/', views.card_register, name='card_register'),
    path('pool/', views.card_pool, name='card_pool'),
    path('del/<int:card_id>/', views.card_del, name='card_del'),

    path('decks/', views.deck_list, name='deck_list'),
    path('decks/add/', views.deck_edit, name='deck_add'), 

    path('proxy/', views.ProxyView.as_view(), name='proxy'),
]
