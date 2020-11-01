import datetime
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
        return 18  # FIXME

    def get_nickname(self):
        return self.nickname or self.first_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, blank=True, default='')
    # order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Document(models.Model):
    STUDY = 'S'
    VACCINE = 'V'
    TYPE_CHOICES = [(STUDY, 'Estudio'), (VACCINE, 'Vacuna')]

    profile = models.ForeignKey('Profile', related_name='documents', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='documents',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=1, default=STUDY, choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, default='')
    tags = models.TextField(blank=True, default='')
    entity = models.TextField(blank=True, default='')
    professional = models.TextField(blank=True, default='')
    public_link = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    @classmethod
    def query(cls, profile, query='', vaccine=False):
        Q = models.Q
        dtype = vaccine and cls.VACCINE or cls.STUDY
        qs = cls.objects.filter(profile=profile, type=dtype)
        for q in query.split():
            q_name = Q(name__icontains=q)
            q_description = Q(description__icontains=q)
            q_entity = Q(entity__icontains=q)
            q_professional = Q(professional__icontains=q)
            q_category = Q(category__name__icontains=q)
            qs = qs.filter(q_name | q_description | q_entity | q_professional | q_category)
        return qs


class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey('Document', related_name='files',
        on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    file = models.FileField(null=True, blank=True)
    profile = models.ForeignKey('Profile', related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Calendar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.created
