# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save

from async_messages import messages

from client.tasks import send_sms
from core.models import User


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(null=True, blank=True)
    intern_code = models.CharField(max_length=45, null=True, blank=True, verbose_name="COD Interno")
    dni = models.CharField(max_length=45, null=True, blank=True, verbose_name="DNI/CIF")

    def __str__(self):
        return self.name.encode('utf8')

    def get_phones(self):
        return Phone.objects.filter(client=self)

    def get_addresses(self):
        return Address.objects.filter(client=self)

    def get_first_address(self):
        return self.get_addresses().first()


class Phone(models.Model):
    alias = models.CharField(max_length=45)
    phone = models.CharField(max_length=45, verbose_name="Teléfono")
    client = models.ForeignKey(Client, related_name="phones")

    def __str__(self):
        return (self.alias + " - " + self.phone).encode('utf8')


class Address(models.Model):
    alias = models.CharField(max_length=45)
    address = models.TextField(verbose_name="Dirección")
    client = models.ForeignKey(Client)
    latitude = models.CharField(max_length=45, null=True, blank=True)
    longitude = models.CharField(max_length=45, null=True, blank=True)
    default_zone = models.ForeignKey('intervention.Zone', null=True)

    def get_url_gmaps(self):

        if self.latitude is not None and self.longitude is not None and self.latitude is not "" \
                and self.longitude is not "":
            return "https://maps.google.com/maps?q=loc:" + self.latitude + "," + self.longitude
        else:
            return False

    def __str__(self):
        return ("(" + self.alias + ") - " + self.address).encode('utf8')


class SMSStatus(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class SMS(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User)
    body = models.TextField(max_length=160)
    sent_status = models.ForeignKey(SMSStatus, default=1)
    phone = models.ForeignKey(Phone)

    def process_phone(self):
        phone_processed = self.phone.phone.replace(" ", "")
        phone_processed = '+34' + phone_processed.replace(".", "")
        if len(phone_processed) == 12:
            return phone_processed
        else:
            return False

    def send(self):
        number = self.process_phone()
        if number:
            import boto3
            from django.conf import settings
            sns = boto3.client('sns',
                               aws_access_key_id=settings.AWS_ACCESS_KEY,
                               aws_secret_access_key=settings.AWS_SECRET_KEY,
                               region_name=settings.AWS_REGION
                               )
            result = sns.publish(PhoneNumber=number, Message=self.body)
            status = int(result['ResponseMetadata']['HTTPStatusCode'])
            if status == 200:
                self.sent_status_id = 2
                dict = {"success": True}
            else:
                self.sent_status_id = 3
                dict = {"success": False, "reason": "error"}
        else:
            self.sent_status_id = 4
            dict = {"success": False, "reason": "incorrect_phone"}

        self.save()
        return dict


def post_save_sms(sender, **kwargs):
    sms = kwargs['instance']
    if kwargs['created']:
        send_sms.delay(sms)


post_save.connect(post_save_sms, sender=SMS)
