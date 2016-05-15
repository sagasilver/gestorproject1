from django.contrib.auth.models import User
from sgpa.models import Rol


def obtenerPermisos(request):
    usuario = request.user
    roles = usuario.roles.all()
    permisosObjects = []
    permisos=[]
    for rolactual in roles:

        permisosObjects.extend(rolactual.permisos.all())
    for permisoObject in permisosObjects:
        permisos.append(permisoObject.nombre)
    return permisos

def obtenerPermisosSistema(request):
    usuario = request.user
    roles = usuario.roles.filter(tipo="SISTEMA")
    permisosObjects = []
    permisos=[]
    for rolactual in roles:

        permisosObjects.extend(rolactual.permisos.all())
    for permisoObject in permisosObjects:
        permisos.append(permisoObject.nombre)
    return permisos


def obtenerPermisosProyecto(request):
    usuario = request.user
    roles = usuario.roles.filter(tipo="PROYECTO")
    permisosObjects = []
    permisos=[]
    for rolactual in roles:

        permisosObjects.extend(rolactual.permisos.all())
    for permisoObject in permisosObjects:
        permisos.append(permisoObject.nombre)
    return permisos

def obtenerRolesAsignados(request, codigo):
    usuarios = User.objects.all()
    rolesObjects = []
    roles=[]
    for usuario in usuarios:
        rolesObjects.append(usuario.roles.all())
    for rolObject in rolesObjects:
        for r in rolObject:
            roles.append(r)
    return roles