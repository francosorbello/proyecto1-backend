from django.urls import path

from UserAPP.views import UserAPPView

urlpatterns = [
    path('user-api/',UserAPPView.as_view()),
    path('user-api/<int:pk>/',UserAPPView.as_view()),
]