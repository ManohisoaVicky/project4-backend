from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListCreate.as_view()),
    # path('new/', views.EventCreate.as_view()),
    path('<int:pk>/', views.EventDetailUpdateDelete().as_view()), 
    path('user/<int:pk>/', views.AllUserEvents.as_view()), 
    path('joined/<int:pk>/', views.JoinedEvents.as_view())
]