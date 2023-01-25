from django.urls import path
from .views import GoogleCalenderInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalenderInitView.as_view(), name="oauth_init"),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name="calenderapi_response"),
]