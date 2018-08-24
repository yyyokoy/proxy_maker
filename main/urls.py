from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.TopView.as_view(), name='index'),
]
