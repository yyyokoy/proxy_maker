from django.conf.urls import url
from accounts import views
from django.urls import include, path

app_name = 'accounts'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('login/', views.Login.as_view(), name='login'),
  path('logout/', views.Logout.as_view(), name='logout'),
  path('user_create/', views.UserCreate.as_view(), name='user_create'),
]
