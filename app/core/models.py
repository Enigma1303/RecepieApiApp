"""
Database models for the application.
"""

import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin      

def recipe_image_file_path(instance,filename):
    """Generate file path for new recipe image"""
    ext=os.path.splitext(filename)[1]
    filename=f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads','recipe',filename)
class UserManager(BaseUserManager):
    """Manager for users."""

#password none so we can create users without passwords for testing and extra fields for future used so without updating we can add more fields
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user."""
        if not email:
            raise ValueError('Users must have an email address')
        #user assigned to this model so we do self.model to create user instance
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        #passing using db to support multiple dbs no need but just in case and good practice
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
        """Create and save a new superuser."""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""
    email = models.EmailField(max_length=255, unique=True)
    name= models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    
class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image=models.ImageField(null=True,upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title   
    
class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name    
    
    
class Ingredient(models.Model):
    """Ingrident for recepies"""
    name=models.CharField(max_length=255)
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.name 
       