from django.contrib import admin
from .models import Usuario, Sucursal, Caja, OSociales, Tarjetas, HistorialCaja
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Sucursal)
admin.site.register(Caja)
admin.site.register(OSociales)
admin.site.register(Tarjetas)
admin.site.register(HistorialCaja)


