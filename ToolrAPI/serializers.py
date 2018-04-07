from rest_framework import serializers

from .models import Message, Picture, Tool, UserProfile
from ToolrAPI.models import UserRating


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        #fields = ('id', 'picture')

class ToolSerializer(serializers.ModelSerializer):

    picture = PictureSerializer(many=True, required=False)
    class Meta:
        model = Tool
        fields = '__all__'
        read_only_fields = ('owner',)

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender',)

class UserProfileSerializer(serializers.ModelSerializer):

    rating = serializers.FloatField(initial=0)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'rating', 'user')


class UserRatingSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UserRating
        fields = ('subject_user', 'rating')
        