from django.contrib import admin

# Register your models here.
from repair.models import AthRepair, IdegisRepair, AthRepairLog, IdegisRepairLog

admin.site.register(AthRepair)
admin.site.register(AthRepairLog)
admin.site.register(IdegisRepair)
admin.site.register(IdegisRepairLog)
