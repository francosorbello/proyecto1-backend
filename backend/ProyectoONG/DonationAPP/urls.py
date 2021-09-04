from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DonationAPPView, DonationStatusView

urlpatterns = [
    path('donation-api/',DonationAPPView.as_view()),
    path('donation-api/<int:pk>/',DonationAPPView.as_view()),
    path('donation-api/status/',DonationStatusView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
