from django.forms.models import model_to_dict
from .models import UserProfile
import json
from django.http import HttpResponse

def getUserProfile(request,id):
    user = UserProfile.objects.get(pk=id)
    data = model_to_dict(user)
    serialized_data = json.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')
