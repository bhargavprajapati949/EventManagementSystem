from django.contrib import admin
from Administrator.models import *
# Register your models here.

admin.site.register(Admin)
# admin.site.register(to_whome_paid)
# admin.site.register(vol_to_admin_pay)
admin.site.register(Payments)
admin.site.register(Sponsers)