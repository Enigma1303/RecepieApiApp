"""
Serializers for the user app.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,)
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
    #we update these serializer in models only for password field to handle encryption
    #otherwise modelserializer will put it as plain text which is not secure
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it."""
        password = validated_data.pop("password", None)
        #using super to call the update method of the parent class which is modelserializer 
        # to update the user instance with the validated data except password
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")
        
        #after authentication we add user to attrs dictionary which can 
        #be accessed later by the view
        attrs["user"] = user
        return attrs    