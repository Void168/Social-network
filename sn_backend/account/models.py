import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('E-mail không hợp lệ!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class Birthday(models.Model):
    date = models.CharField(blank=True, null=True, default='', max_length=255)
    year = models.CharField(blank=True, null=True, default='', max_length=255)
    is_private = models.BooleanField(default=True)
    only_me = models.BooleanField(default=False)
    
class Website(models.Model):
    url = models.CharField(blank=True, null=True, default='', max_length=255)
    is_private = models.BooleanField(default=True)
    only_me = models.BooleanField(default=False)
    
class PhoneNumber(models.Model):
    number = models.CharField(blank=True, null=True, default='', max_length=255)
    is_private = models.BooleanField(default=True)
    only_me = models.BooleanField(default=False)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(validators=[username_validator], blank=True, default='', max_length=255, unique=True)
    display_name = models.CharField(blank=True, default=uuid.uuid1, max_length=255)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images', blank=True, null=True)
    biography = models.CharField(blank=True, default='', max_length=255)
    nickname = models.CharField(blank=True, default='', max_length=255)
    gender = models.CharField(blank=True, default='', max_length=255)
    
    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)
    
    following = models.ManyToManyField('self')
    followers = models.ManyToManyField('self')
    followers_count = models.IntegerField(default=0)
    
    relationship_status = models.CharField(blank=True, default='', max_length=255)
    partner = models.CharField(blank=True, default='', max_length=255)
    
    hometown = models.CharField(blank=True, default='', max_length=255)
    living_city = models.CharField(blank=True, default='', max_length=255)
            
    people_you_may_know = models.ManyToManyField('self')
    
    posts_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def get_avatar(self):
        if self.avatar:
            return 'http://127.0.0.1:8000' + self.avatar.url
        else: 
            return 'https://www.pngkey.com/png/full/115-1150152_default-profile-picture-avatar-png-green.png'
    
    def get_cover_image(self):
        if self.cover_image:
            return 'http://127.0.0.1:8000' + self.cover_image.url
        else: 
            return 'https://th.bing.com/th/id/OIP.o1n4kgruF-5cDCCx7jNYKQHaEo?pid=ImgDet&rs=1'
    def get_displayed_name(self):
        return f"user{self.display_name[:8]}"
    
class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User, related_name='received_friendshiprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_friendshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)
    
class RelationshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User, related_name='received_relationshiprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    relationship_type = models.CharField(max_length=20, default='', blank=True)
    created_by = models.ForeignKey(User, related_name='created_relationshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)