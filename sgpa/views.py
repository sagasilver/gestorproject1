import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime, date, timedelta
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from sgpa.models import  Trabajo, TrabajoForm, HuFormFlujo, AgregarFlujoForm, SprintForm, HuModificarForm, EquipoRolForm, EquipoForm, Equipo, HuFormCambiarEstado,Proyecto,Rol,ClienteFormCambioEstado,UsuarioFormAsignarCliente, ProyectoFormReasignarLider, ProyectoFormCambio,UsuarioFormCambioEstado,ProyectoFormCambioEstado,UsuarioFormAsignarRolSistema,UsuarioFormModificar,Cliente,ClienteForm,ProyectoForm, Flujo, FlujoForm, Actividad,RolProyectoForm, RolSistemaForm, Permiso, Sprint, AsignarHuSprintForm, HuForm, Hu, Historia, \
    Files, SprintFormAsignarHu, HuFormResponsable
from django.db.models import Q
from sgpa.util import obtenerPermisos, obtenerRolesAsignados, obtenerPermisosSistema
from django.core.mail import EmailMessage
import urllib
from django.core.files import File




@login_required()
def nuevo_usuario(request):

    '''
    Permite crear un nuevo usuario en el sistema.
    Solo un usuario con el permiso: "crear usuario", puede llevar a cabo esta operacion.
    Primeramente, se obtiene todos los permisos del usuario que intenta crear el nuevo usuario. Luego,
    se pregunta si el permiso se encuentra dentro de la lista de permisos obtenido. Si resulta verdadero,
    se crea el nuevo usuario, sino, se muestra una p   lantilla indicando que el usuario no posee el permiso
    correspondiente
    @type request:
    @param: request
    @return:
    '''


    permisos = obtenerPermisosSistema(request)

    if "crear usuario" in permisos:
        if request.method == 'POST':
            formulario =  UserCreationForm(request.POST)#, instance=request.user)# Bound form
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:administrar'))
        else:
            formulario =  UserCreationForm()#instance=request.user) # Unbound form

        return render(request, 'nuevoUsuario.html', {'form': formulario, 'permisos':permisos})
    else:
        raiz = "usuario"
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))





@login_required()
def eliminar_usuario(request, codigo):
    '''
    Elimina un usuario del sistema
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de usuarios
    '''
    permisos = obtenerPermisos(request)
    if "eliminar usuario" in permisos:
        bandera=0
        usuario = User.objects.get(pk=codigo)
        proyectos = Proyecto.objects.all()
        for p in proyectos:
            if usuario== p.lider:
                bandera=1
        if bandera==0:
            usuario.delete()
        else:
            mensaje = "El usuario que intenta eliminar es lider de un proyecto"
            return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))
        u = Hu.objects.filter(responsable = usuario)
        if u:
            mensaje = "El usuario que intenta eliminar es responsable de una HU"
            return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse('usuario:administrar'))
    else:
        raiz = "usuario"
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))

@login_required()
def usuario_admin(request):
    '''
    Modulo de administracion de usuarios.
    Permite acceder a las opciones de crear, modificar, eliminar y ver el detalle de los usuarios.
    :param request:
    :return:render_to_response('administrar_usuario.html', {'usuarios':usuarios, 'miusuario':miusuario},context_instance=RequestContext(request))
    '''
    usuario = request.user
    permisos = obtenerPermisos(request)

    if "crear usuario" in permisos or "modificar usuario" in permisos or "eliminar usuario" in permisos:
        miusuario = User.objects.get(username = request.user.username)
        usuarios = User.objects.exclude(username = request.user.username)
        return render_to_response('administrar_usuario.html', {'usuarios':usuarios, 'miusuario':miusuario, 'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = "administracion"
        return render_to_response('sinpermiso.html',{'usuario':usuario, 'raiz':raiz}, context_instance=RequestContext(request))

@login_required()
def modificar_usuario_view( request, id_usuario):
    '''
    Modulo de modificacion de usuarios.
    Permite modificar datos de los usuarios.
    :param request:
    :return:render_to_response('administrar_usuario.html', {'usuarios':usuarios, 'miusuario':miusuario},context_instance=RequestContext(request))
    '''
    permisos = obtenerPermisos(request)
    if "modificar usuario" in permisos:
        usuario= User.objects.get(pk= id_usuario)
        if request.method=="POST":
            formulario= UsuarioFormModificar(request.POST, request.FILES, instance= usuario)
            if formulario.is_valid():
                formulario.save()
                if request.POST.get('password') != "":
                    usuario.password = make_password(request.POST.get('password'), salt=None, hasher='default')
                    usuario.save()
                return HttpResponseRedirect(reverse('usuario:administrar'))
        else:
            formulario= UsuarioFormModificar(instance=usuario)
        return render(request, 'new_modificar_usuario.html', {'formulario':formulario,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = "usuario"
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))



@login_required()
def administrar_rol_de_sistema(request):
    '''
    Modulo de administracion de roles de sistema.
    Permite acceder a las opciones de crear y eliminar roles de sistema.
    :param request:
    :return:render_to_response('administrar_rol_de_sistema.html', {'roles': roles, 'permisos':permisos},context_instance=RequestContext(request))
    '''
    permisos = obtenerPermisosSistema(request)
    if "crear rol sistema" in permisos or "modificar rol sistema" in permisos or "eliminar rol sistema" in permisos or "ver rol sistema" in permisos:
        roles = Rol.objects.filter(tipo="SISTEMA")
        return render_to_response('administrar_rol_de_sistema.html',{'roles': roles, 'permisos':permisos}, context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def nuevo_rol_de_sistema(request):
    '''
    Permite crear un nuevo rol de sistema.
    @param: request
    @return:
    '''
    permisos = obtenerPermisosSistema(request)
    if "crear rol sistema" in permisos:
        if request.method == 'POST':
            formulario =  RolSistemaForm(request.POST)
            if formulario.is_valid():
                r = formulario.save()
                r.tipo = "SISTEMA"
                p_as = Permiso.objects.get(nombre="administrar sistema")
                r.permisos.add(p_as)
                permisos=[]
                permisosObjects = r.permisos.all()
                for permisoObject in permisosObjects:
                    permisos.append(permisoObject.nombre)

                if "crear usuario" in permisos or "modificar usuario" in permisos or "eliminar usuario" in permisos or "ver usuario" in permisos or "asignar rol sistema" in permisos or "cambiar estado usuario" in permisos or "asignar cliente a usuario" in permisos:
                    p_au = Permiso.objects.get(nombre="administrar usuario")
                    r.permisos.add(p_au)

                if "crear proyecto" in permisos or "modificar proyecto" in permisos or "eliminar proyecto" in permisos or "ver proyecto" in permisos or "reasignar lider" in permisos or "cambiar estado proyecto" in permisos:
                    p_ap = Permiso.objects.get(nombre="administrar proyecto")
                    r.permisos.add(p_ap)

                if "crear cliente" in permisos or "modificar cliente" in permisos or "eliminar cliente" in permisos or "cambiar estado cliente" in permisos:
                    p_ac = Permiso.objects.get(nombre="administrar cliente")
                    r.permisos.add(p_ac)

                if "administrar rol sistema" in permisos or "administrar rol proyecto" in permisos:
                    p_ar = Permiso.objects.get(nombre="administrar rol")
                    r.permisos.add(p_ar)

                if "crear rol proyecto" in permisos or "modificar rol proyecto" in permisos or "eliminar rol proyecto" in permisos or "ver rol proyecto" in permisos:
                    p_arp = Permiso.objects.get(nombre="administrar rol proyecto")
                    p_ar = Permiso.objects.get(nombre="administrar rol")
                    r.permisos.add(p_arp)
                    r.permisos.add(p_ar)

                if "crear rol sistema" in permisos or "modificar rol sistema" in permisos or "eliminar rol sistema" in permisos or "ver rol sistema" in permisos:
                    p_ars = Permiso.objects.get(nombre="administrar rol sistema")
                    p_ar = Permiso.objects.get(nombre="administrar rol")
                    r.permisos.add(p_ars)
                    r.permisos.add(p_ar)

                r.save()
                return HttpResponseRedirect(reverse('usuario:adminrolsistema'))
        else:
            formulario =  RolSistemaForm()
        return render(request, 'nuevoRolSistema.html', {'form': formulario, 'permisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def detalle_rol_sistema(request, codigo):
    '''
    Permite ver los datos de un rol de sistema.
    @parameter: request
    @return:render_to_response('detalle_rol_sistema.html', {'rol': rol,'permisos_rol':rol.permisos.all(),'permisos':permisos}
    '''
    permisos = obtenerPermisosSistema(request)
    if "ver rol sistema" in permisos:
        rol = Rol.objects.get(pk=codigo)
        return render_to_response('detalle_rol_sistema.html', {'rol': rol,'permisos_rol':rol.permisos.all(),'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def modificar_rol_sistema(request, codigo):
    permisos = obtenerPermisosSistema(request)
    if "modificar rol sistema" in permisos:
        rol= Rol.objects.get(pk= codigo)
        if request.method=="POST":
            formulario= RolSistemaForm(request.POST, request.FILES, instance= rol)
            if formulario.is_valid():
                r = formulario.save()
                permisosObjects = r.permisos.all()
                permisos=[]

                for permisoObject in permisosObjects:
                    permisos.append(permisoObject.nombre)

                if "crear usuario" in permisos or "modificar usuario" in permisos or "eliminar usuario" in permisos or "ver usuario" in permisos or "asignar rol sistema" in permisos or "cambiar estado usuario" in permisos or "asignar cliente a usuario" in permisos:
                    p_au = Permiso.objects.get(nombre="administrar usuario")
                    r.permisos.add(p_au)
                    p_as = Permiso.objects.get(nombre="administrar sistema")
                    r.permisos.add(p_as)


                if "crear proyecto" in permisos or "modificar proyecto" in permisos or "eliminar proyecto" in permisos or "ver proyecto" in permisos or "reasignar lider" in permisos or "cambiar estado proyecto" in permisos:
                    p_ap = Permiso.objects.get(nombre="administrar proyecto")
                    r.permisos.add(p_ap)
                    p_as = Permiso.objects.get(nombre="administrar sistema")
                    r.permisos.add(p_as)

                if "crear cliente" in permisos or "modificar cliente" in permisos or "eliminar cliente" in permisos or "cambiar estado cliente" in permisos:
                    p_ac = Permiso.objects.get(nombre="administrar cliente")
                    r.permisos.add(p_ac)
                    p_as = Permiso.objects.get(nombre="administrar sistema")
                    r.permisos.add(p_as)

                if "administrar rol sistema" in permisos or "administrar rol proyecto" in permisos:
                    p_ar = Permiso.objects.get(nombre="administrar rol")
                    r.permisos.add(p_ar)
                    p_as = Permiso.objects.get(nombre="administrar sistema")
                    r.permisos.add(p_as)

                if "crear rol proyecto" in permisos or "modificar rol proyecto" in permisos or "eliminar rol proyecto" in permisos or "ver rol proyecto" in permisos:
                    p_arp = Permiso.objects.get(nombre="administrar rol proyecto")
                    p_ar = Permiso.objects.get(nombre="administrar rol")
                    r.permisos.add(p_arp)
                    r.permisos.add(p_ar)
                    p_as = Permiso.objects.get(nombre="administrar sistema")
                    r.permisos.add(p_as)

                if "crear rol sistema" in permisos or "modificar rol sistema" in permisos or "eliminar rol sistema" in permisos or "ver rol sistema" in permisos:
                    p_ars = Permiso.objects.get(nombre="administrar rol sistema")
                    p_ar = Permiso.objects.get(nombre="administrar rol")
                    r.permisos.add(p_ars)
                    r.permisos.add(p_ar)
                    p_as = Permiso.objects.get(nombre="administrar sistema")
                    r.permisos.add(p_as)

                r.save()

                return HttpResponseRedirect(reverse('usuario:adminrolsistema'))
        else:
            formulario= RolSistemaForm(instance=rol)
        return render(request, 'modificar_rol_sistema.html', {'formulario': formulario, 'rol':rol,'permisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def eliminar_rol_sistema(request, codigo):
    '''
    Elimina un rol del sistema
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de usuarios
    '''
    permisos = obtenerPermisosSistema(request)
    if "eliminar rol sistema" in permisos:
        rolesAsignados = obtenerRolesAsignados(request, codigo)
        rol= Rol.objects.get(pk= codigo)
        if rol in rolesAsignados:
            mensaje = "El rol que intenta eliminar pertenece a almenos un usuario"
            return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))
        else:
            rol.delete()
        return HttpResponseRedirect(reverse('usuario:adminrolsistema'))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def administrar_rol_de_proyecto(request):
    permisos = obtenerPermisosSistema(request)
    if "crear rol proyecto" in permisos or "modificar rol proyecto" in permisos or "eliminar rol proyecto" in permisos or "ver rol proyecto" in permisos:
        roles = Rol.objects.filter(tipo="PROYECTO")
        return render_to_response('administrar_rol_de_proyecto.html',{'roles': roles,'permisos':permisos}, context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def nuevo_rol_de_proyecto(request):
    permisos = obtenerPermisosSistema(request)
    if "crear rol sistema" in permisos:
        if request.method == 'POST':
            formulario =  RolProyectoForm(request.POST)
            if formulario.is_valid():
                r = formulario.save()
                r.tipo = "PROYECTO"
                r.save()
                return HttpResponseRedirect(reverse('usuario:adminrolproyecto'))
        else:
            formulario =  RolProyectoForm()
        return render(request, 'nuevoRolProyecto.html', {'form': formulario,'permisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def detalle_rol_proyecto(request, codigo):

    permisos = obtenerPermisosSistema(request)
    if "ver rol proyecto" in permisos:
        rol = Rol.objects.get(pk=codigo)
        return render_to_response('detalle_rol_proyecto.html', {'rol': rol,'permisos_rol':rol.permisos.all(),'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def modificar_rol_proyecto(request, codigo):
    permisos = obtenerPermisosSistema(request)
    if "modificar rol proyecto" in permisos:
        rol= Rol.objects.get(pk= codigo)
        if request.method=="POST":
            formulario= RolProyectoForm(request.POST, request.FILES, instance= rol)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:adminrolproyecto'))
        else:
            formulario= RolProyectoForm(instance=rol)
        return render(request, 'modificar_rol_proyecto.html', {'formulario': formulario, 'rol':rol,'permisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def eliminar_rol_proyecto(request, codigo):
    '''
    Elimina un rol del sistema
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de usuarios
    '''
    permisos = obtenerPermisosSistema(request)
    if "eliminar rol proyecto" in permisos:
        rolesAsignados = obtenerRolesAsignados(request, codigo)
        rol= Rol.objects.get(pk= codigo)
        if rol in rolesAsignados:
            mensaje = "El rol que intenta eliminar pertenece a almenos un usuario"
            return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))
        else:
            rol.delete()
        return HttpResponseRedirect(reverse('usuario:adminrolproyecto'))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def proyecto_admin(request):
    """permite acceder a la interfaz de opciones de administracion para proyectos,\n recibe un @param request que es la
    peticion para realizar cierta operacion. \n@return retorna la lista de proyectos existentes en el sistema"""
    permisos = obtenerPermisos(request)
    if "crear proyecto" in permisos or "modificar proyecto" in permisos or "eliminar proyecto" in permisos:
        proyectos = Proyecto.objects.all()
        return render_to_response('administrar_proyecto.html', {'proyectos': proyectos, 'permisos':permisos},
                              context_instance=RequestContext(request))
    else:
        raiz = "administracion"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def registrarProyecto(request):
    """Permite registrar un nuevo proyecto en el sistema. \nRecibe como @param un request que habilita
    el formulario para completar los datos del proyecto, una vez completado todos los campos obligatorios
    se crea el proyecto \ny @return a la interfaz proyecto, donde ya se visualiza en la lista el nuevo registro """
    permisos = obtenerPermisos(request)
    if "crear proyecto" in permisos:

        clientes = Cliente.objects.all().filter(estado='ACT')
        usuarios = User.objects.all()
        if not clientes:
            mensaje = "No existen clientes activos en el sistema. Debe crear almenos un cliente con estado ACTIVO"
            return render_to_response('error.html',{'mensaje':mensaje}, context_instance=RequestContext(request))
        if request.method == "POST" and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:adminproyecto'))

        elif request.method == 'POST' and 'Guardar' in request.POST:
            if request.POST.get('fechaInicio') < request.POST.get('fechaFin'):
                formulario = ProyectoForm(request.POST)
                if formulario.is_valid():
                    nombre = formulario.cleaned_data['nombre']
                    formulario.save()
                    pro = Proyecto.objects.get(nombre = nombre)
                    pro.fechaInicio = request.POST.get('fechaInicio')
                    pro.fechaFin = request.POST.get('fechaFin')

                    pro.save()
                    return HttpResponseRedirect(reverse('usuario:adminproyecto'))
                else:
                    return render(request, 'nuevoProyecto.html', {'formulario': formulario,'clientes':clientes,'usuarios':usuarios,'permisos':permisos})

            else:
                return render_to_response('datonovalido.html', context_instance=RequestContext(request))
        else:
            formulario = ProyectoForm()
            return render(request, 'nuevoProyecto.html', {'formulario': formulario,'clientes':clientes,'usuarios':usuarios,'permisos':permisos})
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def modificar_proyecto_view(request, id_proyecto):
    '''
    Permite modificar los datos de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    '''
    permisos = obtenerPermisos(request)
    if "modificar proyecto" in permisos:

        proyecto = Proyecto.objects.get(pk=id_proyecto)


        if request.method == 'POST' and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:adminproyecto'))

        elif request.method == 'POST' and 'Guardar' in request.POST:
                if request.POST.get('fechaInicio') > request.POST.get('fechaFin'):
                    return render_to_response('datonovalido2.html', context_instance=RequestContext(request))
                else:
                    formulario= ProyectoFormCambio(request.POST, request.FILES, instance= proyecto)
                    if formulario.is_valid():
                        formulario.save()
                        proyecto = Proyecto.objects.get(pk=id_proyecto)
                        proyecto.fechaInicio = request.POST.get('fechaInicio')
                        proyecto.fechaFin = request.POST.get('fechaFin')
                        proyecto.save()

                        return HttpResponseRedirect(reverse('usuario:adminproyecto'))
                    else:
                        return render(request, 'modificar_proyecto.html', {'formulario':formulario,'proyecto': proyecto, 'permisos':permisos},context_instance=RequestContext(request))
        else:
            formulario= ProyectoFormCambio(instance = proyecto)
            return render_to_response('modificar_proyecto.html', {'formulario':formulario,'proyecto': proyecto,'permisos':permisos},
                  context_instance=RequestContext(request))
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def eliminar_proyecto(request, codigo):
    '''
    Elimina un proyecto del sistema
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de Proyectos
    '''
    permisos = obtenerPermisos(request)
    if "eliminar proyecto" in permisos:
        proyecto = Proyecto.objects.get(pk=codigo)


        proyecto.delete()
        return HttpResponseRedirect(reverse('usuario:adminproyecto'))
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def detalle_proyecto_view_desarrollo( request, id_proyecto):
    '''
    Permite ver el detalle de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    cliente = proyecto.cliente
    equipo = Equipo.objects.filter(proyecto=id_proyecto)
    return render_to_response('detalle_proyecto.html', {'proyecto': proyecto, 'cliente':cliente,'equipo':equipo,'permisos':permisos},context_instance=RequestContext(request))


@login_required()
def detalle_proyecto_view( request, id_proyecto):
    '''
    Permite ver el detalle de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    '''
    permisos = obtenerPermisos(request)
    if "ver proyecto" in permisos:
        proyecto = Proyecto.objects.get(pk=id_proyecto)
        cliente = proyecto.cliente
        equipo = Equipo.objects.filter(proyecto=id_proyecto)
        return render_to_response('detalle_proyecto.html', {'proyecto': proyecto, 'cliente':cliente,'equipo':equipo,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))




@login_required()
def detalle_usuario_view( request, id_usuario):
    '''
    Permite ver el detalle de un usuario
    :param request:
    :param id_usuario:
    :return:
    '''
    permisos = obtenerPermisos(request)
    if "ver usuario" in permisos:
        usuario = User.objects.get(pk=id_usuario)
        return render_to_response('detalle_usuario.html', {'usuario': usuario,'permisos':permisos},
                  context_instance=RequestContext(request))
    else:
        raiz = "usuario"
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))



@login_required()
def cliente_admin(request):
    """permite acceder a la interfaz de opciones de administracion para clientes,\n recibe un @param request que es la
    peticion para realizar cierta operacion. \n@return retorna la lista de proyectos existentes en el sistema"""
    permisos = obtenerPermisos(request)
    if "crear cliente" in permisos or "modificar cliente" in permisos or "eliminar cliente" in permisos:
        clientes = Cliente.objects.all()
        return render_to_response('administrar_cliente.html', {'clientes': clientes, 'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = "administracion"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def nuevo_cliente(request):
    permisos = obtenerPermisos(request)
    if "crear cliente" in permisos:
        if request.method == 'POST':
            formulario = ClienteForm(request.POST)#, instance=request.user)# Bound form
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:admincliente'))
        else:
            formulario = ClienteForm()#instance=request.user) # Unbound form

        return render(request, 'nuevoCliente.html', {'form': formulario,'permisos':permisos})
    else:
        raiz = "cliente"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def detalle_cliente(request, codigo):
    permisos = obtenerPermisos(request)
    if "ver cliente" in permisos:
        cliente = Cliente.objects.get(pk = codigo)
        usuarios = User.objects.filter(cliente=codigo)
        return render_to_response('detalle_cliente.html', {'cliente':cliente, 'usuarios': usuarios,'permisos':permisos},
                  context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def modificar_cliente_view( request, id_cliente):
    '''
    Permite modificar los datos de un cliente
    :param request:
    :param id_cliente:
    :return:
    '''
    permisos = obtenerPermisos(request)
    if "modificar cliente" in permisos:
        cliente = Cliente.objects.get(pk=id_cliente)
        if request.method == 'POST' and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:admincliente'))

        if request.method == 'POST' and 'Guardar' in request.POST:
            if request.POST.get('nombre') != "":
                cliente.nombre = request.POST.get('nombre')
            if request.POST.get('correo') != "":
                cliente.email = request.POST.get('correo')
            if request.POST.get('telefono') != "":
                cliente.telefono = request.POST.get('telefono')
            if request.POST.get("direccion") != "":
                cliente.direccion = request.POST.get('direccion')
            if request.POST.get("observacion") != "":
                cliente.direccion = request.POST.get('observacion')
            cliente.save()
            return HttpResponseRedirect(reverse('usuario:admincliente'))

        return render(request, 'modificar_cliente.html', {'cliente':cliente,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = "cliente"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def eliminar_cliente(request, codigo):
    '''
    Elimina un usuario del sistema
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de cliente
    '''
    permisos = obtenerPermisos(request)
    if "eliminar cliente" in permisos:
        cliente= Cliente.objects.get(pk= codigo)
        proyectos = Proyecto.objects.filter(cliente = codigo)
        usuarios = User.objects.filter(cliente_id = codigo)
        if proyectos:
            mensaje = "El cliente que intenta eliminar es cliente de almenos un proyecto"
            return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))
        if usuarios:
            mensaje = "El cliente que intenta eliminar esta asociado a un usuario"
            return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))

        cliente.delete()
        return HttpResponseRedirect(reverse('usuario:admincliente'))
    else:
        raiz = "cliente"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def administracion(request):
    permisos = obtenerPermisos(request)
    if "crear usuario" in permisos or "modificar usuario" in permisos or "eliminar usuario" in permisos or "crear proyecto" in permisos or "modificar usuario" in permisos or "eliminar usuario" in permisos or "crear cliente" in permisos or "modificar cliente" in permisos or "eliminar cliente" in permisos or "crear rol" in permisos or "modificar rol" in permisos or "eliminar rol" in permisos:
        return render_to_response('administracion.html',{'permisos':permisos},context_instance=RequestContext(request))
    else:
        return render_to_response('sinpermiso.html', context_instance=RequestContext(request))

@login_required()
def gestionar_flujo(request):
    '''
    Modulo de administracion de flujos de sistema.
    Permite acceder a las opciones de crear , modificar y eliminar flujos en el sistema.
    Solo un usuario con el permiso: "crear flujo" o "eliminar flujo"
    puede llevar a cabo esta operacion.

    @param request: request

    @type request: HttpRequest

    @return: request, 'gestionar_flujo.html', {'flujos':flujos, 'permisos':permisos}
    '''
    permisos = obtenerPermisos(request)

    if "crear flujo" in permisos or "ver flujo" in permisos or "modificar flujo" in permisos or "eliminar flujo" in permisos or "agregar flujo" in permisos:
        flujos = Flujo.objects.all()
        return render_to_response('gestionar_flujo.html', {'flujos':flujos, 'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def nuevo_flujo(request):
    '''
    Permite crear un nuevo flujo en el sistema.
    Solo un usuario con el permiso: "crear flujo", puede llevar a cabo esta operacion.

    @param request: request

    @type request: HttpRequest

    @return: request, 'nuevoFlujo.html', {'form': formulario,'permisos':permisos}
    '''

    permisos = obtenerPermisos(request)

    if "crear flujo" in permisos:
        if request.method == 'POST':
            formulario =  FlujoForm(request.POST)#, instance=request.user)# Bound form
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:gestionar_flujo'))
        else:
            formulario =  FlujoForm()#instance=request.user) # Unbound form

        return render(request, 'nuevoFlujo.html', {'form': formulario,'permisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


def detalle_flujo_view( request, id_flujo):
    '''
    Permite ver los datos de un flujo.
    Solo un usuario con el permiso: "ver flujo" puede llevar a cabo esta operacion.

    @param request: request

    @type request: HttpRequest

    @param id_flujo: codigo del flujo

    @type id_flujo: ID de flujo

    @return: 'detalle_flujo.html', {'flujo': flujo, 'actividades':actividades,'permisos':permisos}
    '''
    permisos = obtenerPermisos(request)
    if "ver flujo" in  permisos:
        flujo = Flujo.objects.get(pk=id_flujo)
        actividades = flujo.actividades.all()
        return render_to_response('detalle_flujo.html', {'flujo': flujo, 'actividades':actividades,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def modificar_flujo( request, id_flujo):
    '''
    Permite modificar los datos de un flujo en el sistema.
    Solo un usuario con el permiso: "modificar flujo", puede llevar a cabo esta operacion.

    @param request: request

    @type request: HttpRequest

    @param id_flujo: codigo del flujo a modificar

    @type id_flujo: ID de flujo

    @return: request, 'modificar_flujo.html', {'formulario':formulario,'permisos':permisos}
    '''
    permisos = obtenerPermisos(request)
    if "modificar flujo" in permisos:
        flujo= Flujo.objects.get(pk= id_flujo)
        if request.method=="POST":
            formulario= FlujoForm(request.POST, request.FILES, instance= flujo)
            if formulario.is_valid():
                formulario.save()
        else:
            formulario= FlujoForm(instance=flujo)
        return render(request, 'modificar_flujo.html', {'formulario':formulario,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))




@login_required()
def eliminar_flujo(request, codigo):
    '''
    Permite eliminar un flujo del sistema.
    Solo un usuario con el permiso: "eliminar flujo", puede llevar a cabo esta operacion.

    @param request: request

    @type request: HttpRequest

    @param codigo: codigo del flujo a eliminar

    @type codigo: ID de flujo

    @return: HttpResponseRedirect(reverse('usuario:gestionar_flujo'))
    '''
    permisos = obtenerPermisos(request)
    if "eliminar flujo" in permisos:
        flujo = Flujo.objects.get(pk=codigo)
        proyectos = Proyecto.objects.all()
        bandera = 0
        for proyecto in proyectos:
            if flujo.id in proyecto.flujo.all():
                bandera = 1

        if bandera == 0:
             mensaje = "El flujo que intenta eliminar es utilizado en almenos un proyecto"
             return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))
        else:
             flujo.delete()

        return HttpResponseRedirect(reverse('usuario:gestionar_flujo'))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def agregar_actividad(request,flujo_id):
    '''
    Permite agregar una actividad a un flujo del sistema.
    Solo un usuario con el permiso: "agregar actividad", puede llevar a cabo esta operacion.

    @param request: request

    @type request: HttpRequest

    @param flujo_id: codigo del flujo

    @type flujo_id: ID de flujo

    @return: request, 'agregar_actividad.html',{'permmisos':permisos}
    '''
    permisos = obtenerPermisos(request)
    if "agregar actividad" in permisos:
        if request.method == 'POST' and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:gestionar_flujo'))
        elif request.method == 'POST' and 'Guardar' in request.POST:
            flujo = Flujo.objects.get(pk=flujo_id)
            actividadflujo = flujo.actividades.all()
            cantidad=actividadflujo.count()
            actividad = Actividad(nombre=request.POST.get('nombre'),estado_1='TO_DO',estado_2='DOING',estado_3='DONE',orden=cantidad+1)
            actividad.save()
            flujo.actividades.add(actividad)
            flujo.cantidad=+1
            flujo.save()
            return HttpResponseRedirect(reverse('usuario:gestionar_flujo'))
        else:
            return render(request, 'agregar_actividad.html',{'permmisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def ingresar_Proyecto(request,codigo):
    '''
       Permite ingrear al modulo de desarrollo de un proyecto.
       Solo un usuario con el permiso: "ingresar proyecto", puede llevar a cabo esta operacion.

       @param request: request

       @type request: HttpRequest

       @param codigo: codigo del proyecto

       @type codigo: ID de proyecto

       @return: request, 'ingresar_Proyecto.html', {'proyectos':proyectos,'permisos':permisos,'codigo':codigo}
       '''

    permisos = obtenerPermisos(request)
    usuario = User.objects.get(pk = codigo)
    equipo= Equipo.objects.all().filter(usuario_id = usuario.id)
    proyecto1 = Proyecto.objects.all().filter(lider_id=usuario.id).filter(estado="ACTIVO")
    proyectos = Proyecto.objects.all().filter(estado="ACTIVO")
    return render_to_response('ingresar_Proyecto.html', {'proyectos':proyectos,'proy_lider':proyecto1,'permisos':permisos,'codigo':codigo,'equipos':equipo}, context_instance=RequestContext(request))

@login_required()
def datos_Proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk = id_proyecto)
    permisos = obtenerPermisosSistema(request)
    equipo = Equipo.objects.filter(proyecto = id_proyecto)
    hu = Hu.objects.filter(proyecto = id_proyecto)
    flujo = proyecto.flujo.all()
    return render_to_response('datos_Proyecto.html', { 'flujo':flujo,'hu':hu,'equipo':equipo,'proyecto':proyecto,'codigo':request.user.id,'permisos':permisos}, context_instance=RequestContext(request))

@login_required()
def equipo_trabajo(request, id_proyecto):
    permisos = obtenerPermisos(request)
    equipo_actual = Equipo.objects.filter(proyecto = id_proyecto)
    equipo = Equipo.objects.filter(proyecto = id_proyecto)
    if "asignar equipo" in permisos:
        proyecto = Proyecto.objects.get(pk=id_proyecto)
        formulario = EquipoForm()
        if request.method == 'POST':
            formulario = EquipoForm(request.POST,request.FILES)

            if formulario.is_valid():

                equipo = formulario.save(commit = False)
                equipo.proyecto=proyecto
                agregado = Equipo.objects.filter(proyecto = equipo.proyecto_id).filter(usuario = equipo.usuario_id)
                if agregado:
                    mensaje = "El usuario "+str(equipo)+" ya fue agregado a equipo"
                    return render_to_response('error.html',{'mensaje':mensaje}, context_instance=RequestContext(request))
                else:

                    equipo.save()
                    return HttpResponseRedirect(reverse('usuario:equipo_trabajo', args=(proyecto.id,)))
        return render_to_response('equipo_trabajo.html',{'codigo':request.user.id,'form':formulario,'proyecto':proyecto,'permisos':permisos,'equipo_actual': equipo_actual,'equipo':equipo}, context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def lista_eliminar_miembro(request, id_proyecto):
    '''

    @param request:
    @param id_proyecto:
    @return:
    '''
    permisos = obtenerPermisos(request)
    equipo = Equipo.objects.filter(proyecto = id_proyecto)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if "eliminar miembro" in permisos:
        return render_to_response('lista_eliminar_miembro.html',{'proyecto':proyecto, 'codigo':request.user.id,'permisos':permisos,'equipo': equipo}, context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))

@login_required()
def eliminar_miembro(request, proyect_id, usu_id):

    permisos = obtenerPermisos(request)
    miembro = Equipo.objects.filter(proyecto = proyect_id).filter(usuario = usu_id)
    if "eliminar miembro" in permisos:
        miembro.delete()

        return HttpResponseRedirect(reverse('usuario:lista_eliminar_miembro', args=(proyect_id,)))
    else:
        raiz = "usuario"
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def detalle_equipo(request, id_proyecto):
    '''

    @param request:
    @param id_proyecto:
    @return:
    '''
    permisos = obtenerPermisos(request)
    equipo = Equipo.objects.filter(proyecto = id_proyecto)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if "ver equipo" in permisos:
        return render_to_response('detalle_equipo.html',{'proyecto':proyecto, 'codigo':request.user.id,'permisos':permisos,'equipo': equipo}, context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))



@login_required()
def equipo_rol(request, id_proyecto, id_equipo):
    proyecto = Proyecto.objects.get(pk = id_proyecto)
    equipo = Equipo.objects.get(pk = id_equipo)
    permisos = obtenerPermisos(request)
    if "crear usuario" in permisos:
        if request.method == "POST":
            formulario= EquipoRolForm(request.POST, request.FILES, instance=equipo)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:datos_Proyecto', args=(proyecto.pk,)))
        else:
            formulario= EquipoRolForm(instance= equipo)
        return render(request, 'asignar_rol_a_equipo.html', {
            "form": formulario,"proyecto":proyecto})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def cambiar_estado_de_usuario(request, codigo):
    usuario = User.objects.get(pk=codigo)

    permisos = obtenerPermisosSistema(request)
    if "cambiar estado usuario" in permisos:
        usuario= User.objects.get(pk= codigo)
        if request.method=="POST":
            formulario= UsuarioFormCambioEstado(request.POST, request.FILES, instance= usuario)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:administrar'))
        else:
            formulario= UsuarioFormCambioEstado(instance=usuario)
        return render(request, 'cambiar_estado_de_usuario.html', {'formulario':formulario,'usuario':usuario,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))



@login_required()
def asignar_rol_de_sistema_a_usuario(request, codigo):
 permisos = obtenerPermisos(request)
 usuario = User.objects.get(pk=codigo)
 if "asignar rol sistema" in permisos:
    if request.method == "POST":
        formulario= UsuarioFormAsignarRolSistema(request.POST, request.FILES, instance= usuario)
        if formulario.is_valid():
            ua = formulario.save(commit=False)
            rsa = ua.roles.all()
            ranom=[]
            for ra in rsa:
                ranom.append(ra.nombre)

            un = formulario.save()
            rsn = un.roles.all()
            print("Rol anterior:", ranom)
            print("Rol nuevo:",rsn)

            return HttpResponseRedirect(reverse('usuario:administrar'))
    else:
        formulario= UsuarioFormAsignarRolSistema(instance= usuario)
    return render(request, 'asignar_rol_de_sistema.html', {
        "formulario": formulario,"usuario":usuario,'permisos':permisos
    })
 else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def asignar_rol_de_proyecto(request, id_usuario, codigo):
 permisos = obtenerPermisos(request)
 usuario = User.objects.get(pk=id_usuario)
 proyecto = Proyecto.objects.get(pk=codigo)
 if "crear usuario" in permisos:
    if request.method == "POST":
        formulario= UsuarioFormAsignarRolSistema(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            usu= formulario.save()
            roles = usuario.roles.all().exclude(tipo = "SISTEMA")
            for r in (roles):
                r.proyecto.add(proyecto)
            return HttpResponseRedirect(reverse('usuario:equipo_rol', args=(proyecto.id,)))
    else:
        formulario= UsuarioFormAsignarRolSistema(instance= usuario)
    return render(request, 'asignar_rol_a_equipo.html', {
        "formulario": formulario,"usuario":usuario
    })
 else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def asignar_cliente_a_usuario(request, codigo):
 permisos = obtenerPermisos(request)
 usuario = User.objects.get(pk=codigo)
 es_lider = Proyecto.objects.filter(lider=codigo)
 es_miembro = Equipo.objects.filter(usuario = codigo)
 if not es_lider and not es_miembro:

    if "asignar cliente a usuario" in permisos:
        if request.method == "POST":
            formulario= UsuarioFormAsignarCliente(request.POST, request.FILES, instance= usuario)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:administrar'))
        else:
            formulario= UsuarioFormAsignarCliente(instance= usuario)
        return render(request, 'asignar_cliente_a_usuario.html', {
            "formulario": formulario,"usuario":usuario
        })
    else:
            raiz = ""
            return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))
 else:
     return render_to_response('no_puede_ser_cliente.html',{'usuario':usuario}, context_instance=RequestContext(request))



@login_required()
def cambiar_estado_de_proyecto(request, codigo):
    proyecto = Proyecto.objects.get(pk=codigo)
    permisos = obtenerPermisos(request)
    if "cambiar estado proyecto" in permisos:
        if request.method=="POST":
            formulario= ProyectoFormCambioEstado(request.POST, request.FILES, instance= proyecto)
            if formulario.is_valid():
                formulario.save()
            return HttpResponseRedirect(reverse('usuario:adminproyecto'))
        else:
            formulario= ProyectoFormCambioEstado(instance=proyecto)
        return render(request, 'cambiar_estado_de_proyecto.html', {'formulario':formulario,'proyecto':proyecto,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def reasignar_lider_de_proyecto(request, codigo):
    proyecto = Proyecto.objects.get(pk=codigo)

    permisos = obtenerPermisos(request)
    if "reasignar lider" in permisos:
        if request.method=="POST":
            formulario= ProyectoFormReasignarLider(request.POST, request.FILES, instance= proyecto)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:adminproyecto'))
        else:
            formulario= ProyectoFormReasignarLider(instance=proyecto)
        return render(request, 'reasignar_lider_de_proyecto.html', {'formulario':formulario,'proyecto':proyecto,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))




@login_required()
def cambiar_estado_de_cliente(request, codigo):
    cliente = Cliente.objects.get(pk=codigo)

    permisos = obtenerPermisos(request)
    if "cambiar estado cliente" in permisos:
        if request.method=="POST":
            formulario= ClienteFormCambioEstado(request.POST, request.FILES, instance= cliente)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:admincliente'))
        else:
            formulario= ClienteFormCambioEstado(instance=cliente)
        return render(request, 'cambiar_estado_de_cliente.html', {'formulario':formulario,'cliente':cliente,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))



@login_required()
def nuevo_hu(request,codigo):
    '''
    Crea un hu asiciado a unproyecto
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de hu
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    if "crear proyecto" in permisos:
        if request.method == "POST" and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))
        elif request.method == 'POST' and 'Guardar' in request.POST:
                formulario = HuForm(request.POST)
                if formulario.is_valid():
                    nombre = formulario.cleaned_data['nombre']
                    vn =formulario.cleaned_data['valornegocio']
                    vt =formulario.cleaned_data['valortecnico']
                    prioridad=formulario.cleaned_data['prioridad']
                    priorizacion=((vn + prioridad + 2 * vt) / 4)
                    pro = formulario.save()
                    pro.proyecto_id = codigo
                    pro.priorizacion=priorizacion
                    pro.save()

                    fecha=datetime.now()
                    fecha.strftime("%a %b %d %H:%M %Y")
                    usuario=request.user
                    dato = Historia(usuario=usuario.username,nombre='Crear',fecha=fecha,descripcion='Se Crea el HU',hu=pro)
                    dato.save()
                    mensaje = "Se creo el hu: %s. \nFue creado por: %s" %(nombre, usuario.username)
                    mail = EmailMessage('Creacion de un HU',mensaje,'smtp.gmail.com',['gustavootazu81@gmail.com','rodrigoamarillasanabria@gmail.com','Rfsgold@gmail.com'])
                    mail.send()

                    return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))
                else:
                    return render( request,'nuevoHu.html', {'permisos':permisos,'codigo':request.user.id,'formulario': formulario,'proyecto':proyecto,'permisos':permisos})
        else:
            formulario = HuForm()
            return render( request,'nuevoHu.html',{'permisos':permisos,'codigo':request.user.id,'formulario':formulario,'proyecto':proyecto})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def hu_admin(request,codigo):
    """permite acceder a la interfaz de opciones de administracion para historias de usuario,\n recibe un @param request que es la
    peticion para realizar cierta operacion. \n@return retorna la lista de historias de usuario en el proyecto"""
    proyecto = Proyecto.objects.get(pk=codigo)
    permisos = obtenerPermisos(request)
    if "crear cliente" in permisos or "modificar cliente" in permisos or "eliminar cliente" in permisos:
        hus = Hu.objects.all().filter(proyecto_id= codigo).order_by('-priorizacion')
        return render_to_response('administrar_hu.html', {'codigo':request.user.id,'hus': hus, 'permisos':permisos,'proyecto':proyecto},context_instance=RequestContext(request))
    else:
        raiz = "administracion"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def eliminar_hu(request, id_hu, codigo):
    '''
    Elimina un hu del sistema
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de Hu
    '''
    permisos = obtenerPermisos(request)
    if "eliminar proyecto" in permisos:
        hu = Hu.objects.get(pk=id_hu)
        proyecto = Proyecto.objects.get(pk=codigo)
        if hu.estadorevision == 'PEN':
            hu.delete()
            usuario=request.user
            mensaje = "Se elimino el hu: %s. \nFue eliminado por: %s" %(hu.nombre, usuario.username)
            mail = EmailMessage('Eliminacion  de un HU',mensaje,'smtp.gmail.com',['gustavootazu81@gmail.com','rodrigoamarillasanabria@gmail.com','Rfsgold@gmail.com'])
            mail.send()
        return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def modificar_hu_view( request, id_hu, codigo):
    '''
    Permite modificar los datos de una historia de Usuario
    :param request:
    :param id_hu:
    :return:
    '''
    proyecto = Proyecto.objects.get(pk=codigo)
    permisos = obtenerPermisos(request)
    equipo = Equipo.objects.filter(proyecto=codigo)
    if "modificar usuario" in permisos:
        hu = Hu.objects.get(pk= id_hu)
        if request.method=="POST":
            formulario=HuModificarForm(request.POST, request.FILES, instance=hu)
            if formulario.is_valid():
                vn = formulario.cleaned_data['valornegocio']
                vt = formulario.cleaned_data['valortecnico']
                prioridad = formulario.cleaned_data['prioridad']
                priorizacion = ((vn + prioridad + 2 * vt) / 4)
                pro = formulario.save()
                pro.priorizacion = priorizacion
                pro.estadorevision='PEN'
                pro.estadodesarrolllo='PRO'
                pro.estadoflujo='TOD'
                pro.save()
                fecha=datetime.now()
                fecha.strftime("%a %b %d %H:%M %Y")
                usuario=request.user
                dato = Historia(usuario=usuario.username,nombre='Modificar',fecha=fecha,descripcion='Se Modifica al HU',hu=hu)
                dato.save()
                mensaje = "Se modifico el hu: %s. \nFue modificado por: %s" %(hu.nombre, usuario.username)
                mail = EmailMessage('Modificacion de HU',mensaje,'smtp.gmail.com',['gustavootazu81@gmail.com','rodrigoamarillasanabria@gmail.com','Rfsgold@gmail.com'])
                mail.send()
                return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))
        else:
            formulario= HuModificarForm(instance=hu)
        return render(request, 'modificar_hu.html', {'codigo':request.user.id, 'hu':hu,'permisos':permisos,'formulario':formulario,'proyecto':proyecto,'responsable':equipo},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def asignar_responsable(request,id_hu,codigo):
    '''
    Asocia un usuario a una historia de usuario
    :param request:
    :param codigo:
    :return:vuelve al modulo de administracion de hu
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    responsable = Equipo.objects.filter(proyecto=codigo)
    hu = Hu.objects.get(pk=id_hu)
    if "crear proyecto" in permisos:
        if request.method == "POST" and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))
        elif request.method == 'POST' and 'Guardar' in request.POST:
            hu.responsable = User.objects.get(username=request.POST.get('responsable'))
            hu.save()
            usuario = request.user
            fecha=datetime.now()
            fecha.strftime("%a %b %d %H:%M %Y")
            dato = Historia(usuario=usuario.username,nombre='Asignar Responsable',fecha=fecha,descripcion='Se Asigna un Responsable al HU',hu=hu)
            dato.save()
            return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))
        else:
            return render( request,'asignar_responsable.html',{'proyecto':proyecto,'responsable':responsable,'hu':hu})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def detalle_hu_view( request, id_hu, codigo):
    '''
    Permite ver el detalle de un HU
    :param request:
    :param id_proyecto, id_hu:
    :return:
    '''
    permisos = obtenerPermisos(request)
    if "ver proyecto" in permisos:
        proyecto = Proyecto.objects.get(pk=codigo)
        hu = Hu.objects.get(pk=id_hu)
        return render_to_response('detalle_hu.html', {'permisos':permisos,'codigo':request.user.id, 'proyecto': proyecto, 'hu':hu},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def gestionar_sprint( request,codigo):
    '''
    Modulo de administracion de sprint de un proyecto en el sistema.
    Solo un usuario con el permiso: "crear sprint" o "ver sprint", puede ingresar a este modulo.
    El sistema muestra una lista de todos los sprint de un proyecto del sistema.

    @param request: request

    @type request: HttpRequest

    @param codigo: codigo del proyecto

    @type codigo: ID de proyecto

    @return: request, 'gestionar_sprint.html', {'hay_activo':hay_activo, 'proyecto': proyecto,'sprints':sprints, 'permisos':permisos}
    '''
    proyecto = Proyecto.objects.get(pk=codigo)
    permisos = obtenerPermisos(request)
    hay_activo = Sprint.objects.filter(proyecto_id = codigo).filter(estado = 'ACT')
    if "ver proyecto" in permisos:
        sprints = Sprint.objects.filter(proyecto_id = codigo).order_by('nombre')
        return render_to_response('gestionar_sprint.html', {'hay_activo':hay_activo, 'proyecto': proyecto,'sprints':sprints, 'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def iniciar( request,id_sprint, codigo):
    '''
    Permite pasar a estado activo un sprint de un proyecto en el sistema.
    Solo un usuario con el permiso: "iniciar sprint", puede ingresar a este modulo.
    El sistema muestra una lista de todos los sprint de un proyecto del sistema.

    @param request: request

    @type request: HttpRequest

    @param id_sprint: codigo del sprint

    @type id_sprint: ID de sprint

    @param codigo: codigo del proyecto

    @type codigo: ID de proyecto

    @return: request, HttpResponseRedirect(reverse('usuario:gestionarsprint', args = (codigo,)))
    '''

    proyecto = Proyecto.objects.get(pk=codigo)
    permisos = obtenerPermisos(request)
    hay_activo = Sprint.objects.filter(proyecto_id = codigo).filter(estado = 'ACT')

    if "ver proyecto" in permisos:
        sprint = Sprint.objects.get(pk = id_sprint)
        if sprint.estado == 'INA':
            sprint.estado = 'ACT'
        else:
            sprint.estado = 'INA'
        sprint.save()
        sprints = Sprint.objects.filter(proyecto_id = codigo).order_by('nombre')
        return HttpResponseRedirect(reverse('usuario:gestionarsprint', args = (codigo,)))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def activar_sprint( request, codigo):
    '''
    Permite activar un sprint
    :param request:
    :param codigo:
    :return:
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    sprints = Sprint.objects.all()
    sprint = Sprint()
    claves = []
    for spr in sprints:
        for h in spr.hu.all():
            claves.append(h.id)
    flujos_del_proyecto = proyecto.flujo.all()
    if "crear proyecto" in permisos:
      if flujos_del_proyecto:
        if request.method == "POST" and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:gestionarsprint',args=(proyecto.id,)))
        elif request.method == 'POST' and 'Guardar' in request.POST:
                if request.POST.get('fechaInicio') < request.POST.get('fechaFin'):
                    sprints_actual = Sprint.objects.filter(proyecto = codigo)
                    cantidad = sprints_actual.count()
                    sprint.nombre = "Sprint_"+str(cantidad+1)
                    sprint.fechaInicio = request.POST.get('fechaInicio')
                    sprint.fechaFin = request.POST.get('fechaFin')
                    sprint.proyecto = proyecto
                    formato = "%Y-%m-%d"
                    fecha_desde = datetime.strptime(sprint.fechaInicio, formato)
                    fecha_hasta = datetime.strptime(sprint.fechaFin, formato)
                    difer = fecha_hasta - fecha_desde
                    sprint.duracion = difer.days
                    sprint.save()
                    proyecto.fechaMod = sprint.fechaFin
                    proyecto.save()
                    return HttpResponseRedirect(reverse('usuario:sprintbacklog',args = (sprint.id, codigo)))
                else:
                    return render_to_response('datonovalido.html',context_instance=RequestContext(request))

        return render_to_response('activar_sprint.html', {'codigo':request.user.id, 'permisos':permisos,'proyecto': proyecto},context_instance=RequestContext(request))
      else:
          mensaje = "EL proyecto no contiene flujos. Debe Seleccionar almenos un flujo para crear un sprint"
          return render_to_response('error.html',{'mensaje':mensaje},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))




@login_required()
def sprint_backlog(request, id_sprint, codigo):
    '''
    Permite asignar los hu a un sprint
    :param request:
    :param id_sprint
    :param codigo:
    :return:
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    sprint = Sprint.objects.get(pk=id_sprint)
    equipo_actual = Equipo.objects.filter(proyecto_id=codigo)
    equipo = Equipo.objects.filter(proyecto_id = codigo)
    historias = Hu.objects.filter(proyecto_id = codigo).filter(id__in = sprint.hu.all()).order_by('-priorizacion')
    total_hu = 0
    capacidad = 0
    diferencia = 0
    if historias:
        for h in historias:
            total_hu = total_hu + h.hora
    for e in equipo:
        capacidad = capacidad + e.hora

    diferencia = capacidad - total_hu

    if "ver proyecto" in permisos:

        return render(request, 'sprint_backlog.html', { 'proyecto':proyecto, 'codigo':request.user.id, 'sprint':sprint, 'permisos':permisos, 'capacidad':capacidad, 'total_hu':total_hu, 'diferencia':diferencia,'hus':historias,'equipo_actual':equipo_actual})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def asignar_hu_a_sprint(request, id_proyecto, id_sprint):
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk = id_proyecto)

    sprints = Sprint.objects.all()
    historias_sprints = []
    for sp in sprints:
        historias_sprints.append(sp.hu.all())

    id_sprints = []
    for h_sprint in historias_sprints:
        for h_s in h_sprint:
            id_sprints.append(h_s.id)

    historias = Hu.objects.filter(proyecto_id = id_proyecto).filter(estadorevision = 'APR').exclude(id__in = id_sprints).order_by('priorizacion')

    if "crear proyecto" in permisos:
        if request.method=="POST":

            formulario= SprintFormAsignarHu(request.POST, request.FILES, proyecto = proyecto, claves = id_sprints)
            if formulario.is_valid():
                sprint = Sprint.objects.get(pk = id_sprint)
                hus = formulario.cleaned_data['hu']
                hus_id = []
                for x in hus:
                    hus_id.append(x.id)
                for h in hus:
                    sprint.hu.add(h)
                sprint.save()
                return render(request, 'asignar_responsable_flujo.html', {'hus':hus,'hus_id': hus_id,'codigo':request.user.id, 'permisos':permisos,'proyecto':proyecto,'sprint':sprint},context_instance=RequestContext(request))

        else:
            formulario= SprintFormAsignarHu(proyecto = proyecto, claves = id_sprints)
            hus = Hu.objects.order_by('-priorizacion').filter(proyecto = proyecto).filter(estadorevision = 'APR').exclude(id__in = id_sprints  )
        return render(request, 'asignar_hu_a_sprint.html', {'hus': hus,'codigo':request.user.id, 'permisos':permisos,'formulario':formulario,'proyecto':proyecto},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def editar_responsable(request, id_hu, id_proyecto, id_sprint):
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk = id_proyecto)
    sprint = Sprint.objects.get(pk = id_sprint)
    hu = Hu.objects.get(pk = id_hu)
    historias = Hu.objects.filter(proyecto_id = id_proyecto).filter(id__in = sprint.hu.all())
    equipo = Equipo.objects.filter(proyecto_id = id_proyecto)
    id_usuarios = []
    for e in equipo:
        id_usuarios.append(e.usuario_id)

    if "crear proyecto" in permisos:
        if request.method=="POST":
            formulario = HuFormResponsable(request.POST, request.FILES, claves = id_usuarios, instance = hu)
            if formulario.is_valid():

                formulario.save()
                usuario = request.user
                fecha=datetime.now()
                fecha.strftime("%a %b %d %H:%M %Y")
                dato = Historia(usuario=usuario.username,nombre='Asignar Responsable',fecha=fecha,descripcion='Se Asigna un Responsable al HU',hu=hu)
                dato.save()
                total_hu = 0
                capacidad = 0
                diferencia = 0
                if historias:
                    for h in historias:
                        total_hu = total_hu + h.hora
                    for e in equipo:
                        capacidad = capacidad + e.hora

                diferencia = capacidad - total_hu


                return render(request, 'sprint_backlog.html', { 'proyecto':proyecto, 'codigo':request.user.id, 'sprint':sprint, 'permisos':permisos, 'capacidad':capacidad, 'total_hu':total_hu, 'diferencia':diferencia,'hus':historias})
        else:
            formulario= HuFormResponsable(claves = id_usuarios, instance = hu)

        return render(request, 'editar_responsable.html', {'codigo':request.user.id, 'permisos':permisos,'formulario':formulario,'proyecto':proyecto},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


def HuFormEditarFlujo(POST, FILES, flujos, instance):
    pass


@login_required()
def editar_flujo(request, id_hu, id_proyecto, id_sprint):
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk = id_proyecto)
    sprint = Sprint.objects.get(pk = id_sprint)
    hu = Hu.objects.get(pk = id_hu)
    historias = Hu.objects.filter(proyecto_id = id_proyecto).filter(id__in = sprint.hu.all())
    equipo = Equipo.objects.filter(proyecto_id = id_proyecto)
    flujos = proyecto.flujo.all()

    if "crear proyecto" in permisos:
        if request.method=="POST":
            formulario = HuFormFlujo(request.POST, request.FILES, proyecto = proyecto, instance = hu)
            if formulario.is_valid():

                formulario.save()
                flujo = Flujo.objects.get(pk=hu.flujo_id)
                actividad = flujo.actividades.get(orden=1)
                hu.actividad=actividad
                hu.estadoflujo='TOD'
                hu.save()
                usuario = request.user
                fecha=datetime.now()
                fecha.strftime("%a %b %d %H:%M %Y")
                dato = Historia(usuario=usuario.username,nombre='Asignar a Flujo',fecha=fecha,descripcion='El Hu se asigna a un flujo',hu=hu)
                dato.save()
                total_hu = 0
                capacidad = 0
                diferencia = 0
                if historias:
                    for h in historias:
                        total_hu = total_hu + h.hora
                    for e in equipo:
                        capacidad = capacidad + e.hora

                diferencia = capacidad - total_hu


                return render(request, 'sprint_backlog.html', { 'proyecto':proyecto, 'codigo':request.user.id, 'sprint':sprint, 'permisos':permisos, 'capacidad':capacidad, 'total_hu':total_hu, 'diferencia':diferencia,'hus':historias})
        else:
            formulario= HuFormFlujo(proyecto = proyecto, instance = hu)

        return render(request, 'editar_flujo.html', {'codigo':request.user.id, 'permisos':permisos,'formulario':formulario,'proyecto':proyecto},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))





@login_required()
def responsable(request, id_hu, codigo, id_sprint, hus):


    concat = ""
    hus_id_str = []
    contador = 1;
    for hx in hus:
            if hx == "1" or hx == "2" or hx == "3" or hx == "4" or hx == "5" or hx == "6" or hx == "7" or hx == "8" or hx == "9" or hx == "0":
                concat = concat+str(hx);
            if hx == ',' or hx == ']':
                contador = contador+1
                hus_id_str.append(concat)
                concat = ""
    hus_id = []
    for h_id_str in hus_id_str:
        hus_id.append(int(h_id_str))

    hus = Hu.objects.filter(id__in = hus_id)

    sprint = Sprint.objects.get(pk = id_sprint)
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    responsable = Equipo.objects.filter(proyecto=codigo)
    hu = Hu.objects.get(pk=id_hu)

    sprints = Sprint.objects.all()
    historias_sprints = []
    for sp in sprints:
        historias_sprints.append(sp.hu.all())

    id_sprints = []
    for h_sprint in historias_sprints:
        for h_s in h_sprint:
            id_sprints.append(h_s.id)

    historias = Hu.objects.filter(proyecto_id = proyecto.id).filter(estadorevision = 'APR').exclude(id__in = id_sprints)


    if "crear proyecto" in permisos:

        if request.method == 'POST' and 'Guardar' in request.POST:
            hu.responsable = User.objects.get(username=request.POST.get('responsable'))
            hu.save()
            usuario = request.user
            fecha=datetime.now()
            fecha.strftime("%a %b %d %H:%M %Y")
            dato = Historia(usuario=usuario.username,nombre='Asignar Responsable',fecha=fecha,descripcion='Se Asigna un Responsable al HU',hu=hu)
            dato.save()
            return render(request, 'asignar_responsable_flujo.html', {'hus': hus,'hus_id': hus_id,'codigo':request.user.id, 'permisos':permisos,'proyecto':proyecto,'sprint':sprint},context_instance=RequestContext(request))

        else:
            return render( request,'asignar_responsable.html',{'proyecto':proyecto,'responsable':responsable,'hu':hu})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def flujo(request, id_hu, codigo, id_sprint, hus):


    concat = ""
    hus_id_str = []
    contador = 1;
    for hx in hus:
            if hx == "1" or hx == "2" or hx == "3" or hx == "4" or hx == "5" or hx == "6" or hx == "7" or hx == "8" or hx == "9" or hx == "0":
                concat = concat+str(hx);
            if hx == ',' or hx == ']':
                contador = contador+1
                hus_id_str.append(concat)
                concat = ""
    hus_id = []
    for h_id_str in hus_id_str:
        hus_id.append(int(h_id_str))

    hus = Hu.objects.filter(id__in = hus_id)





    sprint = Sprint.objects.get(pk = id_sprint)
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    responsable = Equipo.objects.filter(proyecto=codigo)
    hu = Hu.objects.get(pk=id_hu)

    sprints = Sprint.objects.all()
    historias_sprints = []
    for sp in sprints:
        historias_sprints.append(sp.hu.all())

    id_sprints = []
    for h_sprint in historias_sprints:
        for h_s in h_sprint:
            id_sprints.append(h_s.id)

    historias = Hu.objects.filter(proyecto_id = proyecto.id).filter(estadorevision = 'APR').exclude(id__in = id_sprints)


    if "crear proyecto" in permisos:
        if request.method=="POST":
            formulario= HuFormFlujo(request.POST, request.FILES, proyecto= proyecto, instance= hu)
            if formulario.is_valid():
                formulario.save()
                flujo = Flujo.objects.get(pk=hu.flujo_id)
                actividad = flujo.actividades.get(orden=1)
                hu.actividad=actividad
                hu.estadoflujo='TOD'
                hu.save()
                usuario = request.user
                fecha=datetime.now()
                fecha.strftime("%a %b %d %H:%M %Y")
                dato = Historia(usuario=usuario.username,nombre='Asignar Flujo',fecha=fecha,descripcion='Se Asigna un flujo al HU',hu=hu)
                dato.save()
                return render(request, 'asignar_responsable_flujo.html', {'hus': hus,'hus_id': hus_id,'codigo':request.user.id, 'permisos':permisos,'proyecto':proyecto,'sprint':sprint},context_instance=RequestContext(request))
        else:
            formulario= HuFormFlujo(proyecto= proyecto, instance=hu)
        return render( request,'asignar_flujo.html',{'formulario':formulario,'proyecto':proyecto,'responsable':responsable,'hu':hu})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def asignar_flujo_sprint(request, id_sprint, codigo):
    '''
    Permite asignar los flujos a un sprint
    :param request:
    :param codigo:
    :return:
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    sprint = Sprint.objects.get(pk=id_sprint)
    if "ver proyecto" in permisos:
        hu = sprint.hu.all()
        return render_to_response('asignar_flujo_sprint.html', {'permisos':permisos, 'codigo':request.user.id, 'hu':hu, 'proyecto':proyecto,'sprint':sprint},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def seleccionar_flujo(request, id_hu, id_sprint, codigo):
    '''
    Permite seleccionar flujos para un HU dentro de un sprint
    :param request:
    :param id_hu:
    :param id_sprint:
    :param codigo:
    :return:
    '''
    hu = Hu.objects.get(pk=id_hu)
    permisos = obtenerPermisos(request)
    if "cambiar estado cliente" in permisos:
        if request.method=="POST":
            formulario= HuFormFlujo(request.POST, request.FILES, proyecto = Proyecto.objects.get(pk = codigo), instance= hu)
            if formulario.is_valid():
                hu = formulario.save()
                flujo = Flujo.objects.get(pk=hu.flujo_id)
                hu.actividad = flujo.actividades.get(orden=1)
                hu.save()
                return HttpResponseRedirect(reverse('usuario:asignarflujosprint',args=(id_sprint, codigo)))
        else:
            formulario= HuFormFlujo(proyecto = Proyecto.objects.get(pk = codigo), instance=hu)
        return render(request, 'seleccionar_flujo.html', {'formulario':formulario,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))



@login_required()
def asignar_hu_sprint(request, id_sprint, codigo):
    '''
    Permite asignar los hu a un sprint
    :param request:
    :param id_sprint
    :param codigo:
    :return:
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    sprint = Sprint.objects.get(pk=id_sprint)

    if "ver proyecto" in permisos:
        if request.method == 'POST':
            formulario =  AsignarHuSprintForm(request.POST,instance = sprint)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:activarsprint',args=(id_sprint,codigo,)))
        else:
            formulario =  AsignarHuSprintForm()
        return render(request, 'asignar_hu_sprint.html', {'formulario': formulario, 'proyecto':proyecto,'sprint':sprint})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def detalle_sprint( request, id_sprint, codigo):
    '''
    Permite ver el detalle de un sprint
    :param request:
    :param id_sprint:
    :param codigo:
    :return:
    '''
    permisos = obtenerPermisos(request)
    sprint = Sprint.objects.get(pk=id_sprint)
    proyecto = Proyecto.objects.get(pk = codigo)
    flujo = proyecto.flujo.all()
    hu = sprint.hu.all()

    return render_to_response('detalle_sprint.html', {'permisos':permisos,'flujo':flujo,'hu':hu,'proyecto':proyecto},context_instance=RequestContext(request))



@login_required()
def cambiar_estado_de_hu( request, id_hu, codigo):
    '''
    Permite cambiar el estado de un hu
    :param request:
    :param  id_hu:
    :param  codigo:
    :return:vuelve al modulo de administracion de hu
    '''
    proyecto = Proyecto.objects.get(pk=codigo)
    permisos = obtenerPermisos(request)
    if "crear usuario" in permisos:

        hu= Hu.objects.get(pk= id_hu)
        if request.method=="POST":
            formulario= HuFormCambiarEstado(request.POST, request.FILES, instance= hu)
            if formulario.is_valid():
                h = formulario.save()
                fecha=datetime.now()
                fecha.strftime("%a %b %d %H:%M %Y")
                usuario=request.user
                dato = Historia(usuario=usuario.username,nombre='Cambiar Estado',fecha=fecha,descripcion='Se cambio el estado a '+ h.estadorevision,hu=hu)
                dato.save()
                return HttpResponseRedirect(reverse('usuario:adminhu',args=(proyecto.id,)))

        else:
            formulario= HuFormCambiarEstado(instance=hu)
        return render(request, 'cambiar_estado_de_hu.html', {'hu':hu,'codigo':request.user.id,'formulario':formulario,'proyecto':proyecto,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))




@login_required()
def finalizar(request,id_hu,codigo):
    '''
    Permite pasar a estado finalizado un hu dentro del kanban en el sistema.
    Solo un usuario con el permiso: "finalizar hu", puede ingresar a este modulo.

    @param request: request

    @type request: HttpRequest

    @param id_hu: codigo del hu

    @type id_hu: ID de hu

    @param codigo: codigo del proyecto

    @type codigo: ID de proyecto

    @return: request, HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    '''
    permisos = obtenerPermisos(request)
    if "crear proyecto" in permisos:
        proyecto =  Proyecto.objects.get(pk=codigo)
        hu = Hu.objects.get(pk=id_hu)
        trabajo = Trabajo()
        sprints = Sprint.objects.all()
        for sprint in sprints:
            if hu.id in sprint.hu.all():
                trabajo.sprint = sprint.nombre
        user = User.objects.get(pk=hu.responsable_id)
        flujo = Flujo.objects.get(pk=hu.flujo_id)
        actividad = Actividad.objects.get(pk=hu.actividad_id)
        trabajo.nombre = 'Finalizar'
        trabajo.nota = 'Se Finalizo el HU'
        trabajo.actor = user.username
        trabajo.hu = hu
        fecha=date.today()
        fecha.strftime("%Y-%m-%d")
        trabajo.fecha = fecha
        trabajo.flujo = flujo.nombre
        trabajo.actividad = actividad.nombre
        trabajo.estado = hu.estadoflujo
        trabajo.save()
        hu.estadodesarrolllo = 'FIN'
        hu.save()
        return HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def historial_hu(request,id_hu,codigo):
    '''
    Permite visualizar el historial de un HU
    :param request:
    :param  id_hu:
    :param  codigo:
    :return:''
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    hu = Hu.objects.get(pk=id_hu)
    historia = Historia.objects.all().filter(hu_id = id_hu)
    if "cambiar estado cliente" in permisos:
            return render( request,'historialhu.html',{'codigo':request.user.id,'proyecto':proyecto,'historia':historia,'hu':hu,'permisos':permisos})
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(username__icontains=query) |
            Q(is_active__icontains=query)
        )
        results = User.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("search.html", {
        "results": results,
        "query": query
    })


login_required()
def agregar_flujo(request, id_proyecto):
    '''
    Permite agregar flujo a un proyecto
    :param request:
    :param  id_proyeto:
    :return:
    '''
    permisos = obtenerPermisos(request)
    if "asignar equipo" in permisos:
        proyecto = Proyecto.objects.get(pk=id_proyecto)
        formulario = AgregarFlujoForm()
        if request.method == 'POST':
            formulario = AgregarFlujoForm(request.POST,request.FILES, instance=proyecto)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect(reverse('usuario:datos_Proyecto', args=(proyecto.id,)))
        return render_to_response('agregar_flujo.html',{'formulario':formulario,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html',{'raiz':raiz}, context_instance=RequestContext(request))


@login_required()
def flujo_proyecto( request,id_proyecto):
    '''
    Permite gestionar un flujo de un proyecto
    :param request:
    :param id_proyecto:
    :return:
    '''
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    permisos = obtenerPermisos(request)
    hu = Hu.objects.filter(proyecto_id = id_proyecto).filter(estadodesarrolllo = 'PRO')
    flujos = proyecto.flujo.all()
    hu_sprint = []
    sprint = Sprint.objects.filter(proyecto_id = id_proyecto)
    for s in sprint:
        if s.estado == 'ACT':
            fecha = datetime.now()
            fecha_f = datetime.strptime(s.fechaFin, "%Y-%m-%d")
            if fecha_f > fecha:
                hu_sprint = s.hu.all()
            else:
                s.estado = 'INA'
                s.save()
    if "ver proyecto" in permisos:
        return render_to_response('flujo_proyecto.html', {'hu_sprint':hu_sprint,'flujos':flujos,'hu':hu,'proyecto':proyecto,'permisos':permisos},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def agregar_trabajo(request,id_hu,codigo):
    '''
    Permite agregar un trabajo a un hu en el tablero kanabn de un proyecto en el sistema.
    Solo un usuario con el permiso: "agregar trabajo", puede ingresar a este modulo.

    @param request: request

    @type request: HttpRequest

    @param id_proyecto: codigo del proyecto

    @type id_proyecto: ID de proyecto

    @return: request, 'agregar_trabajo.html', {'formulario': formulario,'proyecto':proyecto,'permisos':permisos})
    '''
    permisos = obtenerPermisos(request)
    if "crear proyecto" in permisos:
        hu = Hu.objects.get(pk=id_hu)
        flujo = Flujo.objects.get(pk=hu.flujo_id)
        actividad = Actividad.objects.get(pk=hu.actividad_id)
        proyecto =  Proyecto.objects.get(pk=codigo)
        trabajo = Trabajo()
        if request.method == "POST" and 'Cancelar' in request.POST:
            return HttpResponseRedirect(reverse('usuario:flujo_proyecto', args=(proyecto.id,)))
        elif request.method == 'POST' and 'Guardar' in request.POST:
                formulario = TrabajoForm(request.POST, request.FILES, instance=trabajo)
                if formulario.is_valid():
                    if request.POST.get("archivo") != None:
                        nom  = request.POST.get("archivo")
                        nombre = "/home/gustavo/" + nom
                        f = open(nombre,"rb+")
                        archivo = Files(nombre =f.name,dato =  f.read())
                        archivo.save()

                    sprints = Sprint.objects.all()
                    for sprint in sprints:
                        if hu in sprint.hu.all():
                            trabajo.sprint = sprint.nombre

                    user = User.objects.get(pk=hu.responsable_id)
                    trabajo.actor = user.username
                    trabajo.hu = hu
                    fecha=date.today()
                    fecha.strftime("%Y-%m-%d")
                    trabajo.fecha = fecha
                    if request.POST.get("archivo") != None:
                        trabajo.filename = nom
                        trabajo.size = os.path.getsize(nombre)
                        trabajo.archivo = archivo
                        f.close()
                    trabajo.flujo = flujo.nombre
                    trabajo.actividad = actividad.nombre
                    trabajo.estado = hu.estadoflujo
                    trabajo.save()
                    hu.hora_tra =+ trabajo.horas
                    hu.save()

                    return HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
        else:
            formulario = TrabajoForm()
            return render(request, 'agregar_trabajo.html', {'formulario': formulario,'proyecto':proyecto,'permisos':permisos})
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def ver_trabajo_view( request, id_hu, orden):
    '''
    Permite ver el historial de trabajos de un hu en el sistema.
    Solo un usuario con el permiso: "ver trabajo", puede ingresar a este modulo.

    @param request: request

    @type request: HttpRequest

    @param id_hu: codigo del hu

    @type id_hu: ID de hu

    @param orden: campo para ordenar

    @type orden: atributo de trabajo

    @return: request, 'ver_trabajo.html', { 'trabajos':trabajos}
    '''
    permisos = obtenerPermisos(request)
    if "ver proyecto" in permisos:
        h = Hu.objects.get(pk=id_hu)
        if orden == '1':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('nombre')
        if orden == '2':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('fecha')
        if orden == '3':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('nota')
        if orden == '4':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('horas')
        if orden == '5':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('actor')
        if orden == '6':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('hu')
        if orden == '7':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('flujo')
        if orden == '8':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('actividad')
        if orden == '9':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('estado')
        if orden == '10':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('sprint')
        if orden == '11':
            trabajos = Trabajo.objects.all().filter(hu = id_hu).order_by('filename')
        return render_to_response('ver_trabajo.html', { 'trabajos':trabajos,'h':h},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))



@login_required()
def descarga_view(request, id_hu):
        trabajos = Trabajo.objects.all().filter(hu_id = id_hu).exclude(archivo = None)
        return render_to_response('descargar.html', { 'trabajos':trabajos},context_instance=RequestContext(request))

@login_required()
def descargar(request,archivo_id):
    '''
    Permite descargar el archivo seleccionado, perteneciende a algun HU
    :param request:
    :param archivo_id
    :param codigo:
    :return:vuelve al modulo de administracion de hu
    '''
    archivo = Files.objects.get(pk=archivo_id)
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename="sgpa-Download"'
    response.write(archivo.dato)
    return response

@login_required()
def avanzar(request,id_hu,codigo):
    '''
    Permite avanzar el estado de un hu dentro del kanban en el sistema.
    Solo un usuario con el permiso: "avanzar hu", puede ingresar a este modulo.

    @param request: request

    @type request: HttpRequest

    @param id_hu: codigo del hu

    @type id_hu: ID de hu

    @param codigo: codigo del proyecto

    @type codigo: ID de proyecto

    @return: request, HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    '''
    permisos = obtenerPermisos(request)
    if "crear proyecto" in permisos:
        proyecto =  Proyecto.objects.get(pk=codigo)
        hu = Hu.objects.get(pk=id_hu)
        flujo = Flujo.objects.get(pk= hu.flujo_id)
        actividad = Actividad.objects.get(pk= hu.actividad_id)
        actividades = flujo.actividades.all()
        siguiente = actividad.orden + 1
        trabajo = Trabajo()
        sprints = Sprint.objects.all()
        for sprint in sprints:
            if hu.id in sprint.hu.all():
                trabajo.sprint = sprint.nombre
        user = User.objects.get(pk=hu.responsable_id)
        flujo = Flujo.objects.get(pk=hu.flujo_id)
        actividad = Actividad.objects.get(pk=hu.actividad_id)
        trabajo.nombre = 'Avanzar'
        trabajo.nota = 'Cambio de Estado del HU'
        trabajo.actor = user.username
        trabajo.hu = hu
        fecha=date.today()
        fecha.strftime("%Y-%m-%d")
        trabajo.fecha = fecha
        trabajo.flujo = flujo.nombre
        trabajo.actividad = actividad.nombre
        trabajo.estado = hu.estadoflujo
        trabajo.save()


        for a in actividades:
            if a.orden == siguiente:
                activ = a
        if hu.estadoflujo == 'TOD':
            hu.estadoflujo = 'DOI'
        else:
            if hu.estadoflujo == 'DOI':
                hu.estadoflujo = 'DON'
            else:
                hu.estadoflujo = 'TOD'
                hu.actividad = activ
        hu.save()
        if hu.estadoflujo == 'DON'and actividad.orden == flujo.cantidad:
            destino = User.objects.get(pk = proyecto.lider_id)
            mensaje = "El hu: %s ya esta listo para ser finalizado" %(hu.nombre)
            mail = EmailMessage('Hu listo Para su Finalizacion',mensaje,'smtp.gmail.com',[destino.email])
            mail.send()
        return HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def retroceder(request,id_hu,codigo):
    '''
    Permite retroceder el estado de un hu dentro del kanban en el sistema.
    Solo un usuario con el permiso: "avanzar hu", puede ingresar a este modulo.

    @param request: request

    @type request: HttpRequest

    @param id_hu: codigo del hu

    @type id_hu: ID de hu

    @param codigo: codigo del proyecto

    @type codigo: ID de proyecto

    @return: request, HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    '''
    permisos = obtenerPermisos(request)
    if "crear proyecto" in permisos:
        proyecto =  Proyecto.objects.get(pk=codigo)
        hu = Hu.objects.get(pk=id_hu)
        flujo = Flujo.objects.get(pk= hu.flujo_id)
        actividad = Actividad.objects.get(pk= hu.actividad_id)
        actividades = flujo.actividades.all()
        anterior = actividad.orden - 1
        trabajo = Trabajo()
        sprints = Sprint.objects.all()
        for sprint in sprints:
            if hu.id in sprint.hu.all():
                trabajo.sprint = sprint.nombre
        user = User.objects.get(pk=hu.responsable_id)
        flujo = Flujo.objects.get(pk=hu.flujo_id)
        actividad = Actividad.objects.get(pk=hu.actividad_id)
        trabajo.nombre = 'Retroceder'
        trabajo.nota = 'Cambio de Estado del HU'
        trabajo.actor = user.username
        trabajo.hu = hu
        fecha=date.today()
        fecha.strftime("%Y-%m-%d")
        trabajo.fecha = fecha
        trabajo.flujo = flujo.nombre
        trabajo.actividad = actividad.nombre
        trabajo.estado = hu.estadoflujo
        trabajo.save()
        for a in actividades:
            if a.orden == anterior:
                actividad = a
        if hu.estadoflujo == 'DON':
            hu.estadoflujo = 'DOI'
        else:
            if hu.estadoflujo == 'DOI':
                hu.estadoflujo = 'TOD'
            else:
                hu.estadoflujo = 'DON'
                hu.actividad = actividad
        hu.save()
        return HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    else:
        raiz = "proyecto"
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))

@login_required()
def cambiar_flujo(request, id_hu, id_proyecto):
    '''
    Permite cambiar el flujo de un hu dentro del kanban en el sistema.
    Solo un usuario con el permiso: "cambiar flujo", puede ingresar a este modulo.

    @param request: request

    @type request: HttpRequest

    @param id_hu: codigo del hu

    @type id_hu: ID de hu

    @param id_proyecto: codigo del proyecto

    @type id_proyecto: ID de proyecto

    @return: request, HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk = id_proyecto)
    hu = Hu.objects.get(pk = id_hu)
    equipo = Equipo.objects.filter(proyecto_id = id_proyecto)
    flujos = Flujo.objects.all()

    if "crear proyecto" in permisos:
        if request.method=="POST":
            formulario = HuFormFlujo(request.POST, request.FILES, proyecto = proyecto, instance = hu)
            if formulario.is_valid():

                formulario.save()
                flujo = Flujo.objects.get(pk=hu.flujo_id)
                actividad = flujo.actividades.get(orden=1)
                hu.actividad=actividad
                hu.estadoflujo='TOD'
                hu.save()

                usuario = request.user
                fecha=datetime.now()
                fecha.strftime("%a %b %d %H:%M %Y")
                dato = Historia(usuario=usuario.username,nombre='Asignar a Flujo',fecha=fecha,descripcion='El Hu se asigna a un flujo',hu=hu)
                dato.save()

                trabajo = Trabajo()
                sprints = Sprint.objects.all()
                for sprint in sprints:
                    if hu.id in sprint.hu.all():
                        trabajo.sprint = sprint.nombre
                user = User.objects.get(pk=hu.responsable_id)
                flujo = Flujo.objects.get(pk=hu.flujo_id)
                actividad = Actividad.objects.get(pk=hu.actividad_id)
                trabajo.nombre = 'Cambiar Flujo'
                trabajo.nota = 'Cambio de Flujo del HU'
                trabajo.actor = user.username
                trabajo.hu = hu
                fecha=date.today()
                fecha.strftime("%Y-%m-%d")
                trabajo.fecha = fecha
                trabajo.flujo = flujo.nombre
                trabajo.actividad = actividad.nombre
                trabajo.estado = hu.estadoflujo
                trabajo.save()
                sprint = Sprint.objects.get(proyecto= id_proyecto , estado = "ACT")
                hu = sprint.hu.all()

                return HttpResponseRedirect(reverse('usuario:flujo_proyecto',args=(proyecto.id,)))
        else:
            formulario= HuFormFlujo(proyecto = proyecto, instance = hu)


        return render(request, 'editar_flujo.html', {'codigo':request.user.id, 'permisos':permisos,'formulario':formulario,'proyecto':proyecto},context_instance=RequestContext(request))
    else:
        raiz = ""
        return render_to_response('sinpermiso.html', {'raiz':raiz},context_instance=RequestContext(request))


@login_required()
def finalizar_proyecto(request, codigo):
    '''
    Permite finalizar un proyecto.

    @param request: request

    @type request: HttpRequest

    @return: response
    '''
    permisos = obtenerPermisos(request)
    proyecto = Proyecto.objects.get(pk=codigo)
    proyecto.estado = 'FINALIZADO'
    proyecto.save()
    return HttpResponseRedirect(reverse('usuario:adminproyecto'))