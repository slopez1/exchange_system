import base64

from django.db import models


# Create your models here.

class GlobalData(models.Model):
    PENDING = 1
    ACCEPTED = 2
    DENIED = 3
    KNOWN = 4

    SYNC_STATUS_CHOICES = (
        (KNOWN, 'Known'),
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DENIED, 'Denied')
    )
    identifier = models.CharField(max_length=300, unique=True)
    owner = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    endpoint = models.CharField(max_length=1000)
    sync_status = models.IntegerField(choices=SYNC_STATUS_CHOICES, default=KNOWN)

    def __str__(self):
        return "{}: {}".format(self.identifier, self.description)


class ABSSharedData(models.Model):
    # This class must be extended and add the additional fields you want to share.
    identifier = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=1000)
    synchronized = models.BooleanField(default=False)
    created = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.identifier, self.description)


class ExternalRequests(models.Model):
    PENDING = 1
    ACCEPTED = 2
    DENIED = 3

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DENIED, 'Denied')
    )
    requester = models.CharField(max_length=1000)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    synchronized = models.BooleanField(default=False)
    related_data = models.ForeignKey(ABSSharedData, on_delete=models.CASCADE)

    def decode_requester(self):
        return base64.b64decode(self.requester).decode('utf-8')

    def __str__(self):
        return "{}: {}".format(self.related_data.identifier, self.requester)


class Timers(models.Model):
    GLOBAL = 1
    EXTERNAL_REQUEST = 2
    PETITIONS = 3

    TYPE_CHOICES = (
        (GLOBAL, 'Global'),
        (EXTERNAL_REQUEST, 'External request'),
        (PETITIONS, 'Petitions')
    )

    last_sync = models.DateTimeField(null=True, blank=True)
    seconds = models.IntegerField(default=10)
    timer_type = models.IntegerField(unique=True, choices=TYPE_CHOICES)

    def __str__(self):
        return "{}: {}".format(self.timer_type, self.seconds)


###########################
# EXAMPLE EXTEND ABS DATA #
###########################

# class MedicalData(ABSSharedData):
#     name = models.CharField(max_length=30)
#
#
# class Diagnostic(models.Model):
#     medical = models.ForeignKey(MedicalData, on_delete=models.CASCADE)
#     number = models.IntegerField()
#
#
# class SubDiagnostic(models.Model):
#     diagnostic_aux = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
#     number = models.IntegerField()
