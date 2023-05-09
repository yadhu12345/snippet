from django.urls import path
from .views import *

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/refresh/', RefreshAPIView.as_view(), name='token_refresh'),
    path('api/snippets/create/', SnippetCreateView.as_view(), name='snippet-create'),
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', SnippetDetail.as_view(), name='detail'),
    path('taglist/', TagList.as_view(), name='taglist'),
    path('tagdetails/', TagDetails.as_view(), name='tagdetails'),
    path('deletesnippet/<int:id>/', DeleteSnippet.as_view(), name='delete'),
]