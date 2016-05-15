from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',

     url(r'^asignar_rol_de_proyecto/(?P<id_usuario>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.asignar_rol_de_proyecto', name="asignar_rol_de_proyecto"),
     url(r'^detallesprint/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.detalle_sprint', name="detallesprint"),
     url(r'^equipo_rol/(?P<id_proyecto>\d+)/(?P<id_equipo>\d+)/$', 'sgpa.views.equipo_rol', name="equipo_rol"),
     url(r'^descargar/(?P<archivo_id>\d+)/$', 'sgpa.views.descargar', name="descargar"),
     url(r'^descarga_view/(?P<id_hu>\d+)/$', 'sgpa.views.descarga_view', name="descarga_view"),
     url(r'^flujo_proyecto/(?P<id_proyecto>\d+)/$', 'sgpa.views.flujo_proyecto', name="flujo_proyecto"),
     url(r'^agregar_flujo/(?P<id_proyecto>\d+)/$', 'sgpa.views.agregar_flujo', name="agregar_flujo"),
     url(r'^agregar_trabajo/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.agregar_trabajo', name="agregar_trabajo"),
     url(r'^avanzar/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.avanzar', name="avanzar"),
     url(r'^retroceder/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.retroceder', name="retroceder"),
     url(r'^ver_trabajo/(?P<id_hu>\d+)/$', 'sgpa.views.ver_trabajo_view', name="ver_trabajo"),

     url(r'^seleccionar_flujo/(?P<id_hu>\d+)/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.seleccionar_flujo', name="seleccionar_flujo"),
     url(r'^respon/(?P<id_hu>\d+)/(?P<codigo>\d+)/(?P<id_sprint>\d+)/(?P<hus>[^/]+)/$', 'sgpa.views.responsable', name="respon"),
     url(r'^flujo/(?P<id_hu>\d+)/(?P<codigo>\d+)/(?P<id_sprint>\d+)/(?P<hus>[^/]+)/$', 'sgpa.views.flujo', name="flujo"),
     url(r'^editar_responsable/(?P<id_hu>\d+)/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/$', 'sgpa.views.editar_responsable', name="editar_responsable"),
     url(r'^editar_flujo/(?P<id_hu>\d+)/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/$', 'sgpa.views.editar_flujo', name="editar_flujo"),
     url(r'^cambiar_flujo/(?P<id_hu>\d+)/(?P<id_proyecto>\d+)/$', 'sgpa.views.cambiar_flujo', name="cambiar_flujo"),

     url(r'^crearhu/(?P<codigo>\d+)/$', 'sgpa.views.nuevo_hu', name="crearhu"),
     url(r'^gestionarsprint/(?P<codigo>\d+)/$', 'sgpa.views.gestionar_sprint', name="gestionarsprint"),
     url(r'^activarsprint/(?P<codigo>\d+)/$', 'sgpa.views.activar_sprint', name="activarsprint"),
     url(r'^sprintbacklog/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.sprint_backlog', name="sprintbacklog"),
     url(r'^asignarresponsable/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.asignar_responsable', name="asignarresponsable"),

     url(r'^asignarflujosprint/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.asignar_flujo_sprint', name="asignarflujosprint"),
     url(r'^iniciar/(?P<id_sprint>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.iniciar', name="iniciar"),

     url(r'^asignarhusprint/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)/$', 'sgpa.views.asignar_hu_a_sprint', name="asignarhusprint"),
     url(r'^asignarresponsable/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.asignar_responsable', name="asignarresponsable"),
     url(r'^historialhu/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.historial_hu', name="historialhu"),
     url(r'^cambiar_estado_de_hu/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.cambiar_estado_de_hu', name="cambiar_estado_de_hu"),

     url(r'^adminhu/(?P<codigo>\d+)/$', 'sgpa.views.hu_admin', name="adminhu"),
     url(r'^detalle_hu/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.detalle_hu_view', name = "detalle_hu"),
     url(r'^modificar_hu/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.modificar_hu_view', name = "modificar_hu"),
     url(r'^eliminarhu/(?P<id_hu>\d+)/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_hu', name = "eliminarhu"),


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

     url(r'^gestionar_flujo', 'sgpa.views.gestionar_flujo', name="gestionar_flujo"),
     url(r'^crearflujo', 'sgpa.views.nuevo_flujo', name="crearflujo"),
     url(r'^detalle_flujo/(?P<id_flujo>\d+)/$', 'sgpa.views.detalle_flujo_view', name = "detalle_flujo"),
     url(r'^modificar_flujo/(?P<id_flujo>\d+)/$', 'sgpa.views.modificar_flujo', name = "modificar_flujo"),
     url(r'^eliminar_flujo/(?P<codigo>\d+)/$', 'sgpa.views.eliminar_flujo', name = "eliminar_flujo"),
     url(r'^ingresar_Proyecto/(?P<codigo>\d+)/$', 'sgpa.views.ingresar_Proyecto', name = "ingresar_Proyecto"),
     url(r'^datos_Proyecto/(?P<id_proyecto>\d+)/$', 'sgpa.views.datos_Proyecto', name = "datos_Proyecto"),
     url(r'^agregar_actividad/(?P<flujo_id>\d+)/$', 'sgpa.views.agregar_actividad', name = "agregar_actividad"),
     url(r'^crear_usuario', 'sgpa.views.nuevo_usuario', name="crear_usuario")
)
