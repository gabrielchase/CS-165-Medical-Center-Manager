from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class RegularUserManager(BaseUserManager):
    def create_user(self, username, email, mobile_number, landline_number, password=None):
        """ 
        Creates and saves a RegularUser with given information and hashed password
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            mobile_number=mobile_number,
            landline_number=landline_number
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

class RegularUser(AbstractBaseUser):
    """ 
    RegularUser model
    """

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile_number = models.CharField(max_length=40, unique=True)
    landline_number = models.CharField(max_length=40, unique=True)

    objects = RegularUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    
