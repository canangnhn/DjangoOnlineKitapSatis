from django.db import models

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True','Evet'),
        ('False','Hayır'),
    )

    def __str__(self):
        return self.title

    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    company = models.CharField(max_length=150)
    address = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=150)
    smtpserver = models.CharField(blank=True, max_length=150)
    smtpemail = models.CharField(blank=True,max_length=150)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    aboutus = models.TextField(blank=True)
    references = models.TextField(blank=True)
    contact = models.TextField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)





