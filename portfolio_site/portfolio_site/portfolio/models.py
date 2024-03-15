from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

CATEGORIES =  (
    ('Artykuły', 'Artykuły'),
    ('Projekty ze studiów', 'Projekty ze studiów'),
    ('Inne', 'Inne'),
)

class Portfolio(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(Image, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATEGORIES, default=None)

    def __str__(self):
        return str(self.name)
    

class AboutMe(models.Model):
    title = models.CharField(max_length=10000, null=True, blank=True)
    text = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(Image, null=True, blank=True)

    def __str__(self):
        return str(self.title)
    
class Contact(models.Model):
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    facebook_link = models.CharField(max_length=100, null=True, blank=True)
    instagram_link = models.CharField(max_length=100, null=True, blank=True)