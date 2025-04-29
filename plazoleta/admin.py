from django.contrib import admin
from .models import User, Sucursal, Caja, OSociales, Tarjetas
# Register your models here.

admin.site.register(User)
admin.site.register(Sucursal)
admin.site.register(Caja)
admin.site.register(OSociales)
admin.site.register(Tarjetas)


