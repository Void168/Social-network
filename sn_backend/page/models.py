import uuid

from django.db import models
from django.utils import timezone

from account.models import User

# Create your models here.
class Page(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_page = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(blank=True, max_length=50)
    location = models.CharField(blank=True, null=True, max_length=255)
    
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images', blank=True, null=True)
    
    biography = models.CharField(blank=True, null=True, max_length=255)
        
    following = models.ManyToManyField(User, related_name='page_following', blank=True)
    followers = models.ManyToManyField(User, related_name='page_followers', blank=True)
    likes = models.ManyToManyField(User, related_name='page_likes', blank=True)
    
    followers_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)       
    posts_count = models.IntegerField(default=0)
    
    page_type = models.CharField(blank=True, max_length=50)
    business_hours_status = models.CharField(blank=True, max_length=50)
    start_time = models.CharField(blank=True, null=True, max_length=50)
    close_time = models.CharField(blank=True, null=True, max_length=50)
    
    admin = models.ForeignKey(User, related_name='page_admin', on_delete=models.CASCADE)
    moderators = models.ManyToManyField(User, related_name='page_moderators')
    whos_active = models.ManyToManyField(User, related_name='active_moderators')
    
    created_at = models.DateTimeField(default=timezone.now)
    
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