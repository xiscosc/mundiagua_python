from __future__ import unicode_literals
from datetime import date


from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save

from core.tasks import send_message
from core.utils import has_to_change_password


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, pb_token=None, password=None):

        if not email or not first_name or not last_name:
            raise ValueError('Users must have an email address, username, full_name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name= last_name,
            pb_token=pb_token
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, first_name=None, last_name=None, pb_token=None, password=None):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            pb_token=pb_token
        )
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    pb_token = models.CharField(max_length=254, null=True, blank=True)
    order_in_app = models.IntegerField(default=9)
    is_officer = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    has_notification = models.IntegerField(default=0)
    last_password_update = models.DateField(default="2015-01-01")
    phone = models.CharField(max_length=9, blank=True, null=True)
    objects = MyUserManager()
    is_google = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return (self.first_name + " " + self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        return self.get_full_name()

    def is_staff(self):
        return self.is_superuser

    def has_pb(self):
        if self.pb_token is None or self.pb_token is '' or self.pb_token is u"":
            return False
        else:
            return True

    def has_to_change_password(self):
        if self.is_google:
            return False
        else:
            return has_to_change_password(self.last_password_update)

    def update_change_password(self, commit=False):
        self.last_password_update = date.today()
        if commit:
            self.save()

    def get_assigned_interventions(self):
        from intervention.models import Intervention
        return Intervention.objects.filter(assigned=self, status_id=2).count()

    assigned_interventions = property(get_assigned_interventions)


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, blank=False, related_name='%(class)s_from')
    to_user = models.ForeignKey(User, blank=False, related_name='%(class)s_to', verbose_name="Destinatario")
    subject = models.CharField(max_length=200, blank=False, verbose_name="Asunto")
    body = models.TextField(blank=False, verbose_name="Cuerpo del mensaje")


# SIGNALS

def post_save_message(sender, **kwargs):
    if kwargs['created']:
        ins = kwargs['instance']
        ins.to_user.has_notification = 1
        ins.to_user.save()
        body = ins.body+"\n\n"+ins.from_user.get_full_name()
        send_message.delay(ins.pk, body)


post_save.connect(post_save_message, sender='core.Message')