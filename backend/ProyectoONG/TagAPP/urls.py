from django.urls import path

from TagAPP.views import TagAPPView

urlpatterns = [
    path('tag-api/',TagAPPView.as_view()),
    path('tag-api/<int:pk>/',TagAPPView.as_view()),
]