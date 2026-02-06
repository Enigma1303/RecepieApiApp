"""
URL mappings for the user app.
"""

from django.urls import path
from user import views

#reverse is looking for 'user:create' so we need to set app_name
app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"), #URL for creating a new user                        
    path("token/", views.CreateTokenView.as_view(), name="token"), #URL for creating a new auth token
    path("me/", views.ManageUserView.as_view(), name="me"), #URL for managing the authenticated user
]