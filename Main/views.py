from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import requests
from django.conf import settings


class GoogleCalenderInitView(View):
    def get(self, request):
        redirect_uri = settings.REDIRECT_URI_GOOGLE
        client_id = settings.CLIENT_ID
        oauth_scope = "https://www.googleapis.com/auth/calendar"
        oauth2_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}&response_type=code"

        return redirect(oauth2_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        res_code = request.GET.get('code')

        # Configs for Accessing the 'access_token'
        redirect_uri = settings.REDIRECT_URI_GOOGLE
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        grant_type = "authorization_code"

        # Making a POST Request for Google Endpoint for token
        post_data = {
            'code': res_code, 'client_id': client_id,
            'client_secret': client_secret, 'redirect_uri': redirect_uri,
            'grant_type': grant_type
        }
        tokenURL = "https://accounts.google.com/o/oauth2/token"
        response = requests.post(tokenURL, data=post_data)
        # Getting the Access Token from the POST request
        access_token = response.json().get('access_token')

        # Now, Using this Access Token we can get the Events Registered for the Given User
        calender_api_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response_1 = requests.get(calender_api_url, headers=headers)
        user_events = response_1.json().get('items', [])

        # Returning a JSONResponse to a Web Page
        return JsonResponse(user_events, safe=False)