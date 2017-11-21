from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)

from dashboard.models import (
    Service, Product
)

INSTITUTION_CHOICES = ['treatment_center', 'social_hygiene_clinic', 'testing_hub']


class BaseUserManager(BaseUserManager):
    
    def create_user(self, username, email, mobile_number=None, landline_number=None, is_admin=False, password=None):
        """ 
        Creates and saves a RegularUser with given information and hashed password
        """

        if not email or not username:
            raise ValueError('Users must have an email address')
        
        print('Making user\nadmin: {}'.format(is_admin))
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            mobile_number=mobile_number,
            landline_number=landline_number,
            is_admin=is_admin,
            slug=slugify(username)
        )
        print(user)

        user.set_password(password)
        user.save(using=self._db)
        
        return user


class BaseUser(AbstractBaseUser):

    user_id = models.AutoField(primary_key=True)
    
    # Displayed as Institution Name for Administrators
    username = models.CharField(max_length=255, unique=True, null=False)
    
    email = models.EmailField(max_length=255, unique=True, null=False)
    mobile_number = models.CharField(max_length=40, unique=True, null=True)
    landline_number = models.CharField(max_length=40, unique=True, null=True)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    objects = BaseUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def get_profile(self):
        return reverse('users:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.email


class AdministratorDetailsManager(models.Manager):
    
    def create_administrator(self, username, email, mobile_number, landline_number, 
                            open_time, close_time, location, category, staff, additional_info,
                            password=None):
        
        if not email or not username:
            raise ValueError('Administrators must have an email address')

        user = BaseUser.objects.create_user(username, email, mobile_number, landline_number, True, password=password)

        administrator_details = self.model(
            user=user,
            open_time=open_time,
            close_time=close_time,
            location=location,
            category=category,
            staff=staff,
            additional_info=additional_info
        )

        administrator_details.save()

        return administrator_details


class AdministratorDetails(models.Model):
    """ AdministratorDetails model """    

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    open_time = models.CharField(max_length=5, null=True) # '08:00'
    close_time = models.CharField(max_length=5, null=True) # '18:00'
    location = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=21, null=False)
    staff = models.TextField(null=True)
    additional_info = models.TextField(null=True)

    services = models.ManyToManyField(Service, through='AdministratorServices')
    products = models.ManyToManyField(Product, through='AdministratorProducts')
    
    objects = AdministratorDetailsManager()

    def __str__(self):
        return self.user.email


class AdministratorServices(models.Model):

    admin_service_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(AdministratorDetails)
    service = models.ForeignKey(Service)
    description = models.TextField(null=True)
    price = models.FloatField()

    def __str__(self):
        return '{}-{}'.format(self.admin, self.service)


class AdministratorProducts(models.Model):

    admin_product_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(AdministratorDetails)
    product = models.ForeignKey(Product)
    price = models.FloatField(null=True)
    stock = models.IntegerField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.admin, self.product)


class Feedback(models.Model):
    
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    admin = models.ForeignKey(AdministratorDetails, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)
    comment = models.TextField()

    def __str__(self):
        return '{} to {} ({}): {}'.format(self.user, self.admin, self.rating, self.comment)
