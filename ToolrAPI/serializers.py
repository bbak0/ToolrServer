from gdstorage.storage import GoogleDriveStorage
from rest_framework import serializers

from .models import Conversation, Message, Picture, Tool, UserProfile, Loan
from ToolrAPI.models import UserRating


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        #fields = '__all__'
        fields = ('id',)

class ToolSerializer(serializers.ModelSerializer):

    picture = PictureSerializer(many=True, required=False, read_only = True)
    city = serializers.CharField(max_length = 100, read_only = True)
    adress = serializers.CharField(max_length = 100, read_only = True)

    class Meta:
        model = Tool
        fields = '__all__'
        read_only_fields = ('owner', 'location_lat', 'location_lon')

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender',)

class UserProfileSerializer(serializers.ModelSerializer):

    rating = serializers.FloatField(initial=0)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'rating', 'user', 'birthdate', 'adress', 'avatar_url')


class UserRatingSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UserRating
        fields = ('subject_user', 'rating')

class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ('partner', 'last_message', 'partner_display')

class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = '__all__'
        