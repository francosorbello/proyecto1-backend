from django.urls import path

from CampaignAPP.views import CampaignAPPView

urlpatterns = [
    path('campaign-api/',CampaignAPPView.as_view()),
    path('campaign-api/<int:pk>/',CampaignAPPView.as_view()),
]