from django.db import models
from django.utils import timezone
import datetime
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
# Create your models here.

#extra class

def userFiles(instance, filename):
    
    return f'userfolder/user_{instance.profile.user.id}/{filename}'


#

class users(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    uploaded_at = models.DateTimeField(auto_now_add=True)

    storage = models.FloatField(default=25*1024)

    uniLink = models.SlugField(max_length = 100, unique=True, blank=True)

    is_guest = models.BooleanField(default=False)

    is_premium = models.BooleanField(default=False)

    guest_expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.uniLink:
            base = self.user.username or f"guest_{secrets.token_hex(3)}"
            self.uniLink = slugify(base)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.user.username} Profile ' f'at {self.uploaded_at}'
    
    def get_UserOnly(self):
        return f'{self.user.username}'
    
    #makemigrations later
    def is_expired(self):
        return self.is_guest and self.guest_expires_at <= timezone.now()
    
    def time_left_dictionary(self):
        if not self.is_guest: 
            return None
        else:
            seconds = (self.guest_expires_at - timezone.now()).total_seconds()
            
            minutes = seconds / 60

            hours = minutes / 60
            
            time = {"seconds":int(seconds % 60), "minutes":int(minutes % 60), "hours": int(hours)}

            return time
      
    

    class Meta:
        verbose_name = 'User'        
        verbose_name_plural = 'Users'

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['uploaded_at'])
        ]



#FIX
class userMedia(models.Model):

    profile = models.ForeignKey(users, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=userFiles, null=True, blank=True)
    content_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.profile.user.username}  uploaded image' f'at {self.uploaded_at}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)         
        if self.file and not self.file_size:
            self.file_size = self.file.size
            super().save(update_fields=["file_size"])

    class Meta:
        verbose_name = 'User Files'        
        verbose_name_plural = 'User Files' 
        indexes = [
            models.Index(fields=['profile']),
            models.Index(fields=['file']),
            models.Index(fields=['uploaded_at'])
        ]





class userTexts(models.Model):
    profile = models.ForeignKey(users, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} text at {self.uploaded_at}'
    
    class Meta:
        verbose_name = "User Text"
        verbose_name_plural = "User Texts"

        indexes = [
            models.Index(fields=['profile']),
            models.Index(fields=['message']),
            models.Index(fields=['uploaded_at'])
        ]










# when a built in user object is created....
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        users.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.users.save()





  

