from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Doctors(User):
    phone_number = models.CharField(unique=True, max_length=17) 

    class Meta: 
        verbose_name_plural = 'Doctors'

class Patients(User):

    phone_number = models.CharField(unique=True, max_length=17)
    class Meta:
        verbose_name_plural = 'Patients'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 350:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)