from django.contrib import admin

from fabric.models import *

# Register your models here.
admin.site.register(PeerNode)
admin.site.register(OrdererNode)
admin.site.register(Node)
