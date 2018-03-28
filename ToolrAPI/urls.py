from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name="auth"),
    path('get/user/<int:id>', views.getUserProfile, name='getUserProfile')
]
