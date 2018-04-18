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
router.register(r'conversations', views.ConversationViewSet, 'conversations')


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name="auth"),
    #path('get/user/<int:id>', views.getUserProfile, name='getUserProfile'),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^api/', include(router.urls)),
    path('api/rate/delete', views.delete_rating, name='delete_rating'),
    path('api/picture/', views.PictureViewSet.as_view()),
    path('api/get_picture/', views.get_picture,name='get_picture'),
    path('api/loan/propose/<int:tool_id>/', views.proposeLoan, name='propose_loan'),
    path('api/loan/accept/<int:loan_id>/', views.acceptProposal, name = 'accept_proposal'),
    path('api/loan/return/<int:loan_id>/', views.returnTool, name='return_tool'),
    path('api/loan/rateowner/<int:loan_id>/', views.rateOwner, name = 'rate_owner'),
    path('api/loan/rateborrower/<int:loan_id>/', views.rateBorrower, name='rate_borrower'),
    path('api/loan/own_proposals/', views.getOwnProposals),
    path('api/loan/pending_proposals/', views.getPendingProposals),
    path('api/loan/borrowed_tools/', views.getBorrowedTools),
    path('api/loan/lent_tools/', views.getLentTools),
    path('api/loan/lent_list/', views.getLentList),
    path('api/loan/borrowed_list/', views.getBorrowedList),
]
