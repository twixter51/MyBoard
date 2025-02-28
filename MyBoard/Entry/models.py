from django.db import models
from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

#extra class

def userFiles(instance, filename):
    
    return f'userfolder/user_{instance.profile.user.id}/{filename}'


#

class userUploads(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile ' f'at {self.uploaded_at}'
    
    class Meta:
        verbose_name = 'User'        
        verbose_name_plural = 'Users' 



#FIX
class userMedia(models.Model):
    profile = models.ForeignKey(userUploads, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=userFiles, null=True, blank=True)
    content_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username}  uploaded image' f'at {self.uploaded_at}'


    class Meta:
        verbose_name = 'User Files'        
        verbose_name_plural = 'User Files' 



class userTexts(models.Model):
    profile = models.ForeignKey(userUploads, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} text at {self.uploaded_at}'
    
    class Meta:
        verbose_name = "User Text"
        verbose_name_plural = "User Texts"







#import into first model



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userUploads.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.useruploads.save()





  

