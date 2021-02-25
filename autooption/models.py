from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class HostList(models.Model):
    #host info
    hostname = models.CharField(max_length=128, default='')
    hostip = models.IPAddressField(null=False, default='')
    hostuser = models.CharField(max_length=64, null=False, default='')
    hostpasswd = models.CharField(max_length=64, null=False, default='')
    hostport = models.IntegerField(default=22)
    group = models.CharField(max_length=64, null=False, default='')
    zabbixagent = models.BooleanField(default=False)
    elkagent = models.BooleanField(default=False)
    createdate = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.hostip
    class Meta:
        ordering = ['group', 'hostip']


class GroupList(models.Model):
    group = models.CharField(max_length=64, null=False, default='')
    def __unicode__(self):
        return self.group
    class Meta:
        ordering = ['group']


