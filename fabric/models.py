from django.db import models

# Create your models here.


class Node(models.Model):
    host = models.CharField(max_length=1000)
    path_to_tls_ca_cert = models.CharField(max_length=1000)


class OrdererNode(Node):
    tls_host_override = models.CharField(max_length=1000)


class PeerNode(Node):
    pass
