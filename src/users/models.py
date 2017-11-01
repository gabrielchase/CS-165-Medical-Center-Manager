from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

INSTITUTION_CHOICES = ['treatment_center', 'social_hygiene_clinic', 'testing_hub']


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

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    mobile_number = models.CharField(max_length=40, unique=True, null=True)
    landline_number = models.CharField(max_length=40, unique=True, null=True)

    objects = RegularUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email


class AdministratorUserManager(BaseUserManager):
    def create_administrator(self, institution_name, email, mobile_number, landline_number, 
                    open_time, close_time, location, category, staff, additional_info,
                    password=None):
        """ 
        Creates and saves a RegularUser with given information and hashed password
        """

        if not institution_name or not email:
            raise ValueError('Administrators must provide an institution name and email')

        if category not in INSTITUTION_CHOICES:
            raise ValueError('{} is not a valid institution category'.format(category))

        administrator = self.model(
            institution_name=institution_name,
            email=self.normalize_email(email),
            mobile_number=mobile_number,
            landline_number=landline_number,
            open_time=open_time,
            close_time=close_time,
            location=location,
            category=category, 
            staff=staff,
            additional_info=additional_info,
        )

        administrator.set_password(password)
        administrator.save(using=self._db)
        
        return administrator

class AdministratorUser(AbstractBaseUser):
    """ 
    AdministratorUser model
    """    

    admin_id = models.AutoField(primary_key=True)
    institution_name = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    mobile_number = models.CharField(max_length=40, unique=True, null=True)
    landline_number = models.CharField(max_length=40, unique=True, null=True)
    open_time = models.CharField(max_length=5, null=True)
    close_time = models.CharField(max_length=5, null=True)
    location = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=21, null=False)
    staff = models.TextField(null=True)
    additional_info = models.TextField(null=True)

    objects = AdministratorUserManager()

    USERNAME_FIELD = 'institution_name'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.institution_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.institution_name

