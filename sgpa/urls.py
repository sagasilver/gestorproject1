from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',

     url(r'^asignar_rol_de_proyecto/(?P<id_usuario>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.asignar_rol_de_proyecto', name="asignar_rol_de_proyecto"),
     url(r'^detallesprint/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.detalle_sprint', name="detallesprint"),
     url(r'^equipo_rol/(?P<id_proyecto>\d+)/(?P<id_equipo>\d+)/$', 'sgpa.views.equipo_rol', name="equipo_rol"),
     url(r'^descargar/(?P<archivo_id>\d+)/$', 'sgpa.views.descargar', name="descargar"),
      url(r'^flujo_proyecto/(?P<id_proyecto>\d+)/$', 'sgpa.views.flujo_proyecto', name="flujo_proyecto"),


     url(r'^asignarflujosprint/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.asignar_flujo_sprint', name="asignarflujosprint"),






     url(r'^administrar', 'sgpa.views.usuario_admin', name="administrar"),
     url(r'^equipo_trabajo/(?P<id_proyecto>\d+)/$', 'sgpa.views.equipo_trabajo', name="equipo_trabajo"),
     url(r'^lista_eliminar_miembro/(?P<id_proyecto>\d+)/$', 'sgpa.views.lista_eliminar_miembro', name="lista_eliminar_miembro"),
     url(r'^detalle_equipo/(?P<id_proyecto>\d+)/$', 'sgpa.views.detalle_equipo', name="detalle_equipo"),
     url(r'^eliminar_miembro/(?P<proyect_id>\d+)/(?P<usu_id>\d+)/$', 'sgpa.views.eliminar_miembro', name="eliminar_miembro"),
     url(r'^asignar_cliente_a_usuario/(?P<codigo>\d+)/$', 'sgpa.views.asignar_cliente_a_usuario', name="asignar_cliente_a_usuario"),
     url(r'^asignar_rol_de_sistema/(?P<codigo>\d+)/$', 'sgpa.views.asignar_rol_de_sistema_a_usuario', name="asignar_rol_de_sistema"),
     url(r'^cambiar_estado_de_usuario/(?P<codigo>\d+)/$', 'sgpa.views.cambiar_estado_de_usuario', name="cambiar_estado_de_usuario"),
     url(r'^cambiar_estado_de_proyecto/(?P<codigo>\d+)/$', 'sgpa.views.cambiar_estado_de_proyecto', name="cambiar_estado_de_proyecto"),
     url(r'^cambiar_estado_de_cliente/(?P<codigo>\d+)/$', 'sgpa.views.cambiar_estado_de_cliente', name="cambiar_estado_de_cliente"),

     url(r'^reasignar_lider/(?P<codigo>\d+)/$', 'sgpa.views.reasignar_lider_de_proyecto', name="reasignar_lider"),

     url(r'^crearcliente', 'sgpa.views.nuevo_cliente', name="crearcliente"),
     url(r'^adminproyecto', 'sgpa.views.proyecto_admin', name="adminproyecto"),
     url(r'^crearproyecto', 'sgpa.views.registrarProyecto', name="crearproyecto"),
     url(r'^adminrolsistema', 'sgpa.views.administrar_rol_de_sistema', name="adminrolsistema"),
     url(r'^adminrolproyecto', 'sgpa.views.administrar_rol_de_proyecto', name="adminrolproyecto"),
     url(r'^crearrolproyecto', 'sgpa.views.nuevo_rol_de_proyecto', name="crearrolproyecto"),
     url(r'^crearrolsistema', 'sgpa.views.nuevo_rol_de_sistema', name="crearrolsistema"),
     url(r'^modificar_proyecto/(?P<id_proyecto>\d+)/$', 'sgpa.views.modificar_proyecto_view', name = "modificar_proyecto"),
     url(r'^detalle_proyecto_desarrollo/(?P<id_proyecto>\d+)/$', 'sgpa.views.detalle_proyecto_view_desarrollo', name = "detalle_proyecto_desarrollo"),
     url(r'^detalle_proyecto/(?P<id_proyecto>\d+)/$', 'sgpa.views.detalle_proyecto_view', name = "detalle_proyecto"),
     url(r'^detalle_cliente/(?P<codigo>\d+)/$', 'sgpa.views.detalle_cliente', name = "detalle_cliente"),
     url(r'^detalle_rol_proyecto/(?P<codigo>\d+)/$', 'sgpa.views.detalle_rol_proyecto', name = "detalle_rol_proyecto"),
     url(r'^detalle_rol_sistema/(?P<codigo>\d+)/$', 'sgpa.views.detalle_rol_sistema', name = "detalle_rol_sistema"),
     url(r'^detalle_usuario/(?P<id_usuario>\d+)/$', 'sgpa.views.detalle_usuario_view', name = "detalle_usuario"),
     url(r'^modificar_rol_sistema/(?P<codigo>\d+)/$', 'sgpa.views.modificar_rol_sistema', name="modificar_rol_sistema"),
     url(r'^modificar_rol_proyecto/(?P<codigo>\d+)/$', 'sgpa.views.modificar_rol_proyecto', name="modificar_rol_proyecto"),

     url(r'^modificar_usuario/(?P<id_usuario>\d+)/$', 'sgpa.views.modificar_usuario_view', name = "modificar_usuario"),
     url(r'^eliminar_usuario/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_usuario', name = "eliminar_usuario"),
     url(r'^eliminar_rol_proyecto/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_rol_proyecto', name = "eliminar_rol_proyecto"),
     url(r'^eliminar_rol_sistema/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_rol_sistema', name = "eliminar_rol_sistema"),

     url(r'^eliminar_proyecto/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_proyecto', name = "eliminar_proyecto"),
     url(r'^modificar_password/', 'django.contrib.auth.views.password_change', name='modificar_password'),
     url(r'^search', 'sgpa.views.search', name="search"),
     url(r'^admincliente', 'sgpa.views.cliente_admin', name="admincliente"),
     url(r'^administracion', 'sgpa.views.administracion', name="administracion"),

     url(r'^modificar_cliente/(?P<id_cliente>\d+)/$', 'sgpa.views.modificar_cliente_view', name = "modificar_cliente"),
     url(r'^eliminar_cliente/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_cliente', name = "eliminar_cliente"),



     url(r'^ingresar_Proyecto/(?P<codigo>\d+)/$', 'sgpa.views.ingresar_Proyecto', name = "ingresar_Proyecto"),
     url(r'^datos_Proyecto/(?P<id_proyecto>\d+)/$', 'sgpa.views.datos_Proyecto', name = "datos_Proyecto"),

     url(r'^crear_usuario', 'sgpa.views.nuevo_usuario', name="crear_usuario")
)
