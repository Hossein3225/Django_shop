from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .validators import Check_phone_number_is_valid
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserType(models.IntegerChoices):
    customer = 1 , _("customer")
    admin = 2 , _("admin")
    superuser = 3 , _("superuser")

class CustomUserManager(BaseUserManager):

    def create_user(self,email,password ,**extra_fields):
        if not email:
            raise ValueError(_("the email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)   
        extra_fields.setdefault("is_superuser",True)           
        extra_fields.setdefault("is_verified",True)           
        extra_fields.setdefault("is_active",True)       
        extra_fields.setdefault("type",UserType.superuser.value )       

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must have is_staff=True"))   
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must have is_superuser=True"))    

        return self.create_user(email,password,**extra_fields)  


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    type = models.IntegerField(choices=UserType.choices,default=UserType.customer.value)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='custom_user_groups',  # Unique related_name
        related_query_name='custom_user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions',  # Unique related_name
        related_query_name='custom_user',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField("CustomUser",on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11,null=True,blank=True,validators=[Check_phone_number_is_valid])
    image = models.ImageField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.customer.value:
        Profile.objects.create(user=instance,pk=instance.pk)
    
