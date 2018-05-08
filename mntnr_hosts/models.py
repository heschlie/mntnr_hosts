import uuid

from django.db import models
from django.utils.functional import cached_property
from enumfields import EnumIntegerField

from mntnr_hardware.models import Device
from mntnr_hosts import ClusterType, OperatingSystem


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = EnumIntegerField(ClusterType)
    members = models.ManyToManyField('Host')

    @property
    def virtual_machines(self):
        return self.clustervirtualmachine_set.all()

    def __str__(self):
        return 'cluster: {}'.format(self.name)

    def delete(self, *args, **kwargs):
        if self.members.all():
            children = [vm.hostname for vm in self.virtual_machines]
            raise RuntimeError('cannot delete cluster until its VMs have been reassigned: {}'.format(', '.join(children)))
        for member in self.members.all():
            self.members.remove(member)
        self.save()
        super(Cluster, self).delete(*args, **kwargs)


class Environment(models.Model):
    name = models.SlugField(help_text='a short name for this environment')
    hostname_regex = models.CharField(help_text='reges that defines valid host names for this environment', max_length=128)
    description = models.TextField(help_text='(optional) description of the environment', blank=True)
    monitored = models.BooleanField(help_text='shold new hosts in this environment be monitored by default?')

    def __str__(self):
        return 'environment: {}'.format(self.name)


class Role(models.Model):
    name = models.CharField(max_length=128, help_text='host role name', unique=True)
    description = models.CharField(max_length=255, blank=True)

    @property
    def hosts(self):
        hosts = [host.host for host in self.clustervirtualmachine_set.all()]
        hosts += [host.host for host in self.hostvirtualmachine_set.all()]
        hosts += [host.host for host in self.devicevirtualmachine_set.all()]
        return hosts


class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @cached_property
    def instance(self):
        for attr in ['clustervirtualmachine', 'hostvirtualmachine', 'devicehost']:
            if hasattr(self, attr):
                return getattr(self, attr).__str__()
        return 'host {}'.format(self.id)

    @cached_property
    def type(self):
        for attr in ['clustervirtualmachine', 'hostvirtualmachine', 'devicehost']:
            if hasattr(self, attr):
                return type(getattr(self, attr))

    def __str__(self):
        return 'host {}'.format(id)


class HostBase(models.Model):
    hostname = models.CharField(max_length=256, help_text='Fully qualified domain name', unique=True)
    environment = models.ForeignKey('Environment')
    roles = models.ManyToManyField('Role', blank=True)
    operating_system = EnumIntegerField(OperatingSystem)
    host = models.OneToOneField('Host', on_delete=models.CASCADE, null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    @cached_property
    def domain(self):
        components = self.hostname.split('.')
        return '.'.join(components[1:])

    @cached_property
    def rolenames(self):
        return sorted([role.name for role in self.roles.all()])

    @cached_property
    def shortname(self):
        return self.hostname.split('.')[0]

    def __str__(self):
        return self.hostname

    def delete(self, *args, **kwargs):
        self.host.delete()
        super(HostBase, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.host:
            self.host = Host.objects.create()
        super(HostBase, self).save(*args, **kwargs)


class ClusterVirtualMachine(HostBase):
    parent = models.ForeignKey('Cluster')


class HostVirtualMachine(HostBase):
    parent = models.ForeignKey('DeviceHost')


class DeviceHost(HostBase):
    parent = models.ForeignKey(Device)
