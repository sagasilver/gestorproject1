
__author__ = 'luis'
#! /usr/bin/python


#ejecutar asi ./manage.py shell < script.py

from django.contrib.auth.models import User
from django.contrib.auth.forms import User
from sgpa.models import Proyecto
from sgpa.models import Rol
from sgpa.models import Cliente
from sgpa.models import Permiso
import os, datetime


#Se vacian las tablas
def vaciar():
    Proyecto.objects.all().delete()
    Cliente.objects.all().delete()    
    User.objects.all().delete()




def cargarCliente():

   """Script de carga de Usuarios al sistema"""
   cliente1 = Cliente(nombre='NIKE', direccion='ddscdc', telefono='sdfdsfd', observacion='weewfe', estado='ACT')
   cliente1.save()
   cliente2 = Cliente(nombre='PUMA', direccion='ddscdc', telefono='sdfdsfd', observacion='weewfe', estado='ACT')
   cliente2.save()
   



def cargarUsuario():

   """Script de carga de Usuarios al sistema"""
   usuario2 = User.objects.create_user(username='administrador',password='123')
   


def cargarPermiso():
    """
        Script de carga de permiso para el sistema.
    """
    permiso1 = Permiso(nombre='crear rol sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar rol sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar rol sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear cliente', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar cliente', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar cliente', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver cliente', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver rol sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar flujo', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar flujo', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear flujo', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver flujo', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='agregar actividad', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='asignar equipo', descripcion ='creae rol sistema', tipo='PROYECTO')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar rol proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar rol sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar rol', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='administrar cliente', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='ver rol proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='crear rol proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='modificar rol proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='eliminar rol proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='cambiar estado cliente', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='reasignar lider', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='cambiar estado proyecto', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='asignar cliente a usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='asignar rol sistema', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='cambiar estado usuario', descripcion ='creae rol sistema', tipo='SISTEMA')
    permiso1.save()
    permiso1 = Permiso(nombre='activar sprint', descripcion ='creae rol sistema', tipo='PROYECTO')
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


