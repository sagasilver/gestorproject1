
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from sgpa.util import obtenerPermisos, obtenerPermisosSistema


def ingresar(request):

    '''
    controla si el usuario se encuentra registrado, permite iniciar sesion
    \n@param request:
    \n@return retorna a la siguiente intefaz
    C{import} Importa variables.
    C{variables} todas las variables.
    :param request:
    :return:
    '''

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            nombreDeUsuario = request.POST['username']
            password = request.POST['password']
            usuario = authenticate(username=nombreDeUsuario, password=password)
            if usuario is not None:
                if usuario.is_active:
                    login(request, usuario)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario,}, context_instance=RequestContext(request))

@login_required()
def privado(request):
    """recibe un @param request
        Permite acceder a los servicos del sistema.
    \n@return a la interfaz principal"""
    usuario = request.user
    permisos = obtenerPermisos(request)

    return render_to_response('privado.html', {'usuario':usuario,'permisos':permisos},context_instance=RequestContext(request))

@login_required()
def cerrar(request):
    """funcion que cierra la sesion de un usuario registrado y logeado en el sistema, \nrecibe como @param un request
    y \n@return a la interfaz de inicio sesion"""
    logout(request)
    return HttpResponseRedirect('/')

