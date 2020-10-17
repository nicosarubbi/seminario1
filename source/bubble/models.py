from django.db import models
from utils.fields import OneToOneField


class Profile(models.Model):
    user = OneToOneField('auth.User', related_name='profile', on_delete=models.CASCADE)
    parent = models.ForeignKey('Profile', related_name='childs', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    nickname = models.CharField(max_length=60, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    birthdate = models.DateField(null=True, blank=True)

    @property
    def age(self):
        return 10  # FIXME

    def get_nickname(self):
        return self.nickname or self.first_name


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, blank=True, default='')


class Document(models.Model):
    profile = models.ForeignKey('Profile', related_name='documents', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='documents',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, default='')
    tags = models.TextField(blank=True, default='')
    entity = models.TextField(blank=True, default='')
    professional = models.TextField(blank=True, default='')
    public_link = models.TextField(blank=True, default='')


class File(models.Model):
    document = models.ForeignKey('Document', related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(null=True, blank=True)
    ftype = models.CharField(max_length=6, blank=True, default=True)


class Observation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

