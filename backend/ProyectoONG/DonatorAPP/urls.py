from django.urls import path

from .views import DonatorAPPView

urlpatterns = [
    path('donator-api/',DonatorAPPView.as_view()),
    path('donator-api/<int:pk>/',DonatorAPPView.as_view()),
]