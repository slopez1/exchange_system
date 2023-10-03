from django.contrib import admin

from core.models import *

# Register your models here.

admin.site.register(GlobalData)
admin.site.register(ABSSharedData)
admin.site.register(ExternalRequests)
admin.site.register(Timers)


admin.site.register(Expedient)
admin.site.register(Medication)
admin.site.register(MedicalHistory)





