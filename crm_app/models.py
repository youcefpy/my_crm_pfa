
from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.core.validators import EmailValidator
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.



#creating a custom user 
class User(AbstractUser):
     pass

class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    
    SOURCE_CHOICES = (
        ('Youtube','Youtube'),
        ('Google','Goole'),
        ('Newsletter','Newsletter'),
        ('Facebook','Facebook'),
        ('Instagram','Instagram'),
        ('TikTok','TikTok'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = models.EmailField(validators=[EmailValidator()])
    age = models.IntegerField(null=True, blank=True)

    phoned = models.BooleanField(default=False)
    source = models.CharField(choices=SOURCE_CHOICES,max_length=100)

    profile_picture = models.ImageField(null=True, blank=True,upload_to='leads/')
    file_field = models.FileField(null=True, blank=True,upload_to='documents/')

    agent = models.ForeignKey(Agent,on_delete=models.CASCADE)

    def __str__(self):
        return f"prenom : {self.first_name} | nom: {self.last_name}"