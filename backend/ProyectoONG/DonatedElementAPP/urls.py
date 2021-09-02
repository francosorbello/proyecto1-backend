from django.urls import path

from .views import DonatedElementAPPView

urlpatterns = [
    path('donatedElement-api/',DonatedElementAPPView.as_view()),
    path('donatedElement-api/<int:pk>/',DonatedElementAPPView.as_view()),
]