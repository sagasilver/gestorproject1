
#! /usr/bin/python


#ejecutar asi ./manage.py shell < script.py

from django.contrib.auth.models import User
from django.contrib.auth.forms import User
from sgpa.models import Proyecto
from sgpa.models import Rol
from sgpa.models import Cliente
from sgpa.models import Permiso
import os, datetime


#vaciamos las tablas proyecto, cliente, usaurio
def vaciar():
    Proyecto.objects.all().delete()
    Cliente.objects.all().delete()    
    User.objects.all().delete()




def cargarCliente():

   """Los clientes son cargados al sistema"""
   cliente1 = Cliente(nombre='Grupo Cartes', direccion='ddscdc', telefono='sdfdsfd', observacion='weewfe', estado='ACT')
   cliente1.save()
   cliente2 = Cliente(nombre='AJ.Vierci', direccion='ddscdc', telefono='sdfdsfd', observacion='weewfe', estado='ACT')
   cliente2.save()
   



def cargarUsuario():

   """Los usuarios son cargados al sistema"""

   usuario2 = User.objects.create_user(username='administrador',password='123')
   


def cargarPermiso():
    """
         Los Script son cargados directamente.
    """
    permiso1 = Permiso(nombre='crear rol sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar rol sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar rol sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear cliente', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar cliente', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar cliente', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver cliente', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver rol sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar flujo', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar flujo', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear flujo', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver flujo', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='agregar actividad', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='asignar equipo', descripcion ='crear rol sistema', tipo='PROYECTO')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar rol proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar rol sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar rol', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar cliente', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver rol proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear rol proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar rol proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar rol proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='cambiar estado cliente', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='reasignar lider', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='cambiar estado proyecto', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='asignar cliente a usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='asignar rol sistema', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='cambiar estado usuario', descripcion ='crear rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='activar sprint', descripcion ='crear rol sistema', tipo='PROYECTO')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar miembro', descripcion ='puede eliminar miembros del equipo de trabajo', tipo='PROYECTO')
    permiso1.save()
    permiso1 = Permiso(nombre='gestionar sprint', descripcion ='creae rol sistema', tipo='PROYECTO')
    permiso1.save()
    permiso1 = Permiso(nombre='ver equipo', descripcion ='puede ver los detalles de un equipo de trabajo', tipo='PROYECTO')
    permiso1.save()

def cargarRol():
    permisos = Permiso.objects.all()
    rol = Rol(nombre='Administrador', descripcion='administrador', tipo='SISTEMA')
    rol.save()
    for p in permisos:
        rol.permisos.add(p)
    rol.save()
    user = User.objects.get(pk=1)
    user.roles.add(rol)





"""Empieza la ejecucion"""

print ("Cargando datos en la base de datos...")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
vaciar()
cargarUsuario()
cargarPermiso()
cargarRol()
cargarCliente()


