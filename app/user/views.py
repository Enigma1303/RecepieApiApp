"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions    
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from  user.serializers import (
    UserSerializer,
    AuthTokenSerializer,)

#this createapiview is what the view is based on to create a new user
#handles a http post request to create a new user
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer   
    ##once it knows the serializer class it will handle the rest of the logic 
    #as mentioned in the serializers file
    
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    #by default obtainauthtoken view does not have any renderer classes
    #so we add default renderer classes to it so that we can view it in the browsable api    
    
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    #called in get method so we override it to return the authenticated user
    #this helps as we dont have to pass any user id in the url to get the user details 
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user    
    

           
    