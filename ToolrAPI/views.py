from django.contrib.auth.models import User
from django.core.files import File
from django.db.models import Avg, Q
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from gdstorage.storage import GoogleDriveStorage
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, NotFound
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message, Tool, UserProfile, UserRating
from .serializers import MessageSerializer, PictureSerializer, ToolSerializer
from ToolrAPI.models import Picture
from ToolrAPI.serializers import ConversationSerializer, \
    UserProfileSerializer, UserRatingSerializer
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from google.auth.transport import requests
from google.oauth2 import id_token


#android
CLIENT_ID = "598921763095-u9953ph467i798ackeqt1dq1q4av203a.apps.googleusercontent.com"
#web
CLIENT_ID2 = "598921763095-9dt10r1bgb7vj20gtutvm9ot15fq5v0l.apps.googleusercontent.com"
gd_storage = GoogleDriveStorage()

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
            return HttpResponseBadRequest(e)
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
        user_id = self.request.query_params.get('user_id', None)
        if user_id is None:
            raise NotFound('no parameter found')
        queryset = Message.objects.filter(
                                        (Q(sender = self.request.user) &
                                        Q(recipient_id = user_id))) | Message.objects.filter(Q(recipient = self.request.user) &
                                        Q(sender_id = user_id))
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        conv = Conversation.objects.filter(user = self.request.user, partner_id = self.request.data['recipient'])
        if not conv:
            partnerq = UserProfile.objects.get(user_id = self.request.data['recipient'])
            userq = UserProfile.objects.get(user = self.request.user)
            partnerd = partnerq.first_name + ' ' + partnerq.last_name
            userd = userq.first_name + ' ' + userq.last_name
            Conversation.objects.create(user = self.request.user,
                                        partner_id = self.request.data['recipient'],
                                        partner_display = partnerd,
                                        last_message = self.request.data['message'])
            Conversation.objects.create(user_id = self.request.data['recipient'],
                                        partner = self.request.user,
                                        partner_display = userd,
                                        last_message = self.request.data['message'])
        else:
            conv1 = Conversation.objects.get(user = self.request.user,
                                    partner_id = self.request.data['recipient'])
            conv2 = Conversation.objects.get(user_id = self.request.data['recipient'],
                                        partner = self.request.user)
            conv1.last_message = self.request.data['message']
            conv2.last_message = self.request.data['message']
            conv1.save()
            conv2.save()                            

    def perform_update(self, serializer):
        serializer.save(sender=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(user = self.request.user)


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

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is None:
            raise NotFound('no parameter found')
        try:
            rating = UserRating.objects.filter(subject_user_id = user_id)
        except UserRating.DoesNotExist:
            raise NotFound('no existing rating found')
        return rating

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
        raise NotFound('no existing rating found')
    
    rating.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_picture(request):
    pid = request.data['id']
    if pid is not None:
        try:
            picm = Picture.objects.get(pk=pid)
        except Picture.DoesNotExist:
            raise NotFound('picture not found')
        dupex = gd_storage.open(picm.picture.url)
        print(repr(dupex))
    return Response(status=status.HTTP_204_NO_CONTENT)



class PictureViewSet(APIView):

    parser_classes = (MultiPartParser, )
    def post(self, request, format='jpg'):
        picture = request.FILES['file']
        print(request.data)
        Picture.objects.create(picture = picture, tool_id = request.data['tool_id'])
        return Response(picture.name, status.HTTP_201_CREATED)

    def get(self, request, format=None):
        try:
            url = Picture.objects.get(pk = request.GET.get('pid'))
        except Picture.DoesNotExist:
            raise NotFound('picture not found')
        a = url.picture.name
        dupex = gd_storage.open(a)
        print(repr(dupex))
        return HttpResponse(dupex, content_type="image/jpeg")

    def delete(self, request):
        try:
            url = Picture.objects.get(pk = request.GET.get('pid'))
        except Picture.DoesNotExist:
            raise NotFound('picture not found')
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

