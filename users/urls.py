from django.urls import path 
from . import views

urlpatterns = [
    path("signup/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("<int:pk>/", views.UserDetailUpdate.as_view())
]