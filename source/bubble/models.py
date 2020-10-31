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
    
    vaccine = models.ForeignKey('VaccineDose', related_name='documents', on_delete=models.CASCADE,
                                null=True, blank=True)

    def __str__(self):
        return self.name


class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey('Document', related_name='files',
        on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    file = models.FileField(null=True, blank=True)
    profile = models.ForeignKey('Profile', related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Observation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Calendar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.created


class Vaccine(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    note_number = models.IntegerField(null=True, blank=True)
    note = models.TextField(blank=True, default='')
    exclusive = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    @property
    def title(self):
        if self.note_number:
            return f"{self.name} ({self.note_number})"
        return self.name

    def get_note_text(self):
        return f"({self.note_number}) {self.note}"


class VaccineAge(models.Model):
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=20, blank=True, default='')
    small_title = models.TextField(blank=True, default='')
    months = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        if self.title:
            return self.title
        if self.age:
            return f"{self.age} años"
        return f"{self.months} meses"


class VaccineDose(models.Model):
    vaccine = models.ForeignKey('Vaccine', on_delete=models.CASCADE, related_name='doses')
    age = models.ForeignKey('VaccineAge', on_delete=models.CASCADE, related_name='doses')
    text = models.CharField(max_length=50)
    note_letter = models.CharField(max_length=1, blank=True, default='')
    note_text = models.TextField(blank=True, default='')
    cells = models.IntegerField(default=1)

    def __str__(self):
        if self.note_letter:
            return f"{self.text} {self.note_letter}"
        return self.text






