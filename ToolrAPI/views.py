from django.contrib.auth.models import User
from django.db.models import Avg, Q
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message, Tool, UserProfile, UserRating
from .serializers import MessageSerializer, PictureSerializer, ToolSerializer
from ToolrAPI.models import Picture
from ToolrAPI.serializers import UserProfileSerializer, UserRatingSerializer
from django.http import HttpResponse, JsonResponse
from google.auth.transport import requests
from google.oauth2 import id_token


#android
CLIENT_ID = "598921763095-u9953ph467i798ackeqt1dq1q4av203a.apps.googleusercontent.com"
#web
CLIENT_ID2 = "598921763095-9dt10r1bgb7vj20gtutvm9ot15fq5v0l.apps.googleusercontent.com"

def index(request):
    return render(request, 'ToolrAPI/index.html')

@csrf_exempt
def register(request):
    token = None
    newuser  = None
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
            if not User.objects.filter(username=userid).exists():
                newuser = User.objects.create_user(username=userid, password=userid)
                newuser.save()
                uprofile = UserProfile(user = newuser)
                uprofile.first_name = idinfo['given_name']
                uprofile.last_name = idinfo['family_name']
                uprofile.email = idinfo['email']
                uprofile.google_id = userid
                uprofile.save()

        except ValueError as e:
            print(e)
            return HttpResponse(400)
    token = Token.objects.get(user=newuser)
    print(token.key)

    response = HttpResponse()
    response['token'] = token

    return response


class UserToolsViewSet(viewsets.ModelViewSet):
    serializer_class = ToolSerializer

    def get_queryset(self):
        user = self.request.user
        return Tool.objects.filter(owner = user)

'''
class PictureViewSet(viewsets.ModelViewSet):
    serializer_class = PictureSerializer

"""
    API endpoint that allows to retrieve arbitrary tool
    Parameters:
    "id" - id of the tool

    """
    '''
class ArbitraryToolViewSet(viewsets.ModelViewSet):
    serializer_class = ToolSerializer
    queryset = Tool.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    
    def get_queryset(self):
        return Message.objects.filter(sender = self.request.user) | Message.objects.filter(recipient = self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        serializer.save(sender=self.request.user)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        '''queryset = UserProfile.objects.all()
        for profile in queryset:
            user = profile.user
            ratingset = UserRating.objects.filter(subject_user = user)
            if len(ratingset) == 0:
                profile.rating = 0
            else:
                rsum = 0
                for rating in ratingset:
                    rsum = rsum + rating.rating
                profile.rating = rsum / float(len(ratingset))
        for profile in queryset:
            print(profile.rating)
            '''
        return UserProfile.objects.annotate(rating=Avg('user__rated_user__rating'))

class UserRatingViewSet(viewsets.ModelViewSet):

    serializer_class = UserRatingSerializer
    queryset = UserRating.objects.all()

    def perform_create(self, serializer):
        serializer.save(rating_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(rating_user=self.request.user)

@api_view(['DELETE'])
def delete_rating(request):
    print(request.user)
    print(request.data)
    rating = None
    try:
        rating = UserRating.objects.get(subject_user_id = request.data['subject_user'], rating_user = request.user)
    except UserRating.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    rating.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class PictureViewSet(APIView):

    parser_classes = (MultiPartParser, )
    def post(self, request, format='jpg'):
        picture = request.FILES['file']
        print(request.data)
        Picture.objects.create(picture = picture, tool_id = request.data['tool_id'])
        return Response(picture.name, status.HTTP_201_CREATED)

    def get(self, request, format=None):
        url = Picture.objects.get(pk=2)
        a = url.picture.url
        print(url.picture.file_data)
        return Response({'url' : url.picture.url})