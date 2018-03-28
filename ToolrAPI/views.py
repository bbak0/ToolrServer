from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import UserProfile, AuthToken
from django.utils import timezone
from .auth import *
from .endpoints import *
#android
CLIENT_ID = "598921763095-u9953ph467i798ackeqt1dq1q4av203a.apps.googleusercontent.com"
#web
CLIENT_ID2 = "598921763095-9dt10r1bgb7vj20gtutvm9ot15fq5v0l.apps.googleusercontent.com"

# Create your views here.
def index(request):
    return HttpResponse("Nothing to see here")

@csrf_exempt
def auth(request):
    token = None
    print("request received")
    if request.method == 'POST':
        token = request.POST.get('token')

        try:
    # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID2)
            print(idinfo)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            print(userid)
            if not UserProfile.objects.filter(pk=userid).exists():
                create_user(idinfo)
            token = get_auth_token(userid)
        except ValueError as e:
            print(e)
            return HttpResponse(400)


    response = HttpResponse()
    response['token'] = token

    return response

#currently bugged: creates new token when one already exists



def create_user(idinfo):
    new_user = UserProfile.objects.create(first_name = idinfo['given_name'],
                                        last_name = idinfo['family_name'],
                                        email = idinfo['email'],
                                        google_id = idinfo['sub'])
