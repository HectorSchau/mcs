from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menucaja", views.menucaja, name="menucaja"),
    path("reportecaja", views.reportecaja, name="reportecaja"),
    path("ingresocaja", views.ingresocaja, name="ingresocaja"),
    path("crear_caja", views.crear_caja, name="crear_caja"),
    path("crear_caja2", views.crear_caja2, name="crear_caja2"),
    path('crear_caja3/', views.crear_caja3, name='crear_caja3'), 
    path('reporte_caja_sucursal/', views.reporte_caja_sucursal, name='reporte_caja_sucursal'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
