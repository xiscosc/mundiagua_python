# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save


class InterventionStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name.encode('utf8')


class Zone(models.Model):
    name = models.CharField(max_length=50)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name.encode('utf8')


class Intervention(models.Model):
    description = models.TextField(verbose_name="Descripción")
    address = models.ForeignKey('client.Address', verbose_name="Dirección")
    date = models.DateTimeField(auto_now_add=True)
    zone = models.ForeignKey(Zone, default=1, verbose_name="Zona")
    status = models.ForeignKey(InterventionStatus, default=1)
    created_by = models.ForeignKey('core.User', related_name='%(class)s_by')
    assigned = models.ForeignKey('core.User', null=True, related_name='%(class)s_assigned')
    note = models.TextField(null=True)

    def __str__(self):
        return "V"+str(self.pk)

    def get_history(self):
        return InterventionLog.objects.filter(intervention=self)

    def get_modifications(self):
        return InterventionModification.objects.filter(intervention=self)


class InterventionModification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True)
    created_by = models.ForeignKey('core.User')
    intervention = models.ForeignKey(Intervention)


class InterventionLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('core.User', related_name='%(class)s_by')
    assigned = models.ForeignKey('core.User', null=True, related_name='%(class)s_assigned')
    status = models.ForeignKey(InterventionStatus)
    intervention = models.ForeignKey(Intervention)


def post_save_intervention(sender, **kwargs):
    if kwargs['created']:
        ins = kwargs['instance']
        log = InterventionLog(created_by=ins.created_by, status=ins.status, intervention=ins)
        log.save()
    else:
        pass

post_save.connect(post_save_intervention, sender=Intervention)