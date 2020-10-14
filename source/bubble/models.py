from django.db import models


class Profile(models.Model):
    phone = models.CharField(max_length=20, blank=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField('auth.User', related_name='profile', on_delete=models.CASCADE)

    @property
    def age(self):
        return 10  # FIXME
