from django.urls import path
from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_framework_views
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'user_tools', views.UserToolsViewSet, 'user_tools')
router.register(r'tool', views.ArbitraryToolViewSet, 'tool')
router.register(r'message', views.MessageViewSet, 'message')
router.register(r'userprofile', views.UserProfileViewSet)
router.register(r'rate', views.UserRatingViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name="auth"),
    #path('get/user/<int:id>', views.getUserProfile, name='getUserProfile'),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^api/', include(router.urls)),
    path('api/rate/delete', views.delete_rating, name='delete_rating')
]
