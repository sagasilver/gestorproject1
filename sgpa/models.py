from django.contrib.admin.widgets import AdminDateWidget
from django.db import models, __all__
from django.forms import ModelForm, PasswordInput, DateField, CheckboxSelectMultiple
from django import forms
from django.contrib.auth.models import User, Group
from time import  time

User.add_to_class('direccion', models.TextField(blank=True))
User.add_to_class('telefono', models.CharField(max_length=15, null=True,blank=True))


class Permiso(models.Model):
    TIPO_CHOICES=(
        ('SISTEMA','Sistema'),
        ('PROYECTO','Proyecto')

    )
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=120)
    tipo = models.CharField(max_length=8, blank= False,
                              choices=TIPO_CHOICES,default="SISTEMA"
                              )
    def __unicode__(self):
        return self.nombre



class Actividad(models.Model):
    nombre = models.CharField(max_length=60, unique=False)
    estado_1 = models.CharField(max_length=5,default="TO_DO")
    estado_2 = models.CharField(max_length=5, default="DOING")
    estado_3 = models.CharField(max_length=5,default="DONE")
    orden = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nombre



class Flujo(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=200, unique=True)
    actividades = models.ManyToManyField(Actividad, related_name='actividades')
    cantidad = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nombre


class FlujoForm(forms.ModelForm):
    class Meta:
        model = Flujo
        fields = ('nombre', 'descripcion')


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ('nombre',)


class Cliente(models.Model):
    ESTADO_CHOICES=(
        ('ACTIVO','Activo'),
        ('INACTIVO','Inactivo')
    )
    nombre = models.CharField(max_length=32, unique=True)
    direccion = models.CharField(max_length=70)
    telefono = models.CharField(max_length=70)
    observacion = models.TextField(max_length=200)
    correo = models.CharField(max_length=70)
    estado =  models.CharField(max_length=20,
                              choices=ESTADO_CHOICES,
                              default='ACT')
    def __unicode__(self):
        return self.nombre


User.add_to_class('cliente', models.ForeignKey(Cliente, blank=True, null=True, default=""), )


class Rol(models.Model):
    TIPO_CHOICES=(
        ('SISTEMA','Sistema'),
        ('PROYECTO','Proyecto')

    )
    nombre = models.CharField(max_length=60, unique=True, blank=False)
    descripcion= models.CharField(max_length=120, blank=False)
    tipo = models.CharField(max_length=8, blank= False,
                              choices=TIPO_CHOICES
                              )
    permisos = models.ManyToManyField(Permiso)

    def __unicode__(self):
        return self.nombre

class Proyecto(models.Model):
    ESTADO_CHOICES=(
        ('PENDIENTE','Pendiente'),
        ('ANULADO','Anulado'),
        ('ACTIVO','Activo'),
        ('FINALIZADO','Finalizado')
    )
    fechaInicio = models.CharField(max_length=20)
    fechaFin= models.CharField(max_length=20)
    fechaMod= models.CharField(max_length=20)
    nombre = models.CharField(max_length=32, unique=True, blank=False)
    estado = models.CharField(max_length=20,blank=False,
                              choices=ESTADO_CHOICES,
                              default='PENDIENTE')
    lider= models.ForeignKey(User, related_name='lider',null=True)
    cliente = models.ForeignKey(Cliente,default="")
    flujo = models.ManyToManyField(Flujo, related_name='flujopro')

    def __unicode__(self):
        return self.nombre

class ProyectoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['lider'].queryset = User.objects.all().exclude(cliente__in = Cliente.objects.all())
        for field in self.fields:
            self.fields[field].error_messages = {'required':'Este campo es obligatorio'}
    class Meta:
        model = Proyecto
        fields = ('nombre','cliente','lider')


class ProyectoFormCambio(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProyectoFormCambio, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required':'Este campo es obligatorio'}
    class Meta:
        model = Proyecto
        fields = ('nombre',)


class ProyectoFormCambioEstado(ModelForm):
    class Meta:
        model = Proyecto
        fields=("estado",)




class ProyectoFormReasignarLider(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProyectoFormReasignarLider, self).__init__(*args, **kwargs)
        self.fields['lider'].queryset = User.objects.all().exclude(cliente__in = Cliente.objects.all())
        for field in self.fields:
            self.fields[field].error_messages = {'required':'Este campo es obligatorio'}
    class Meta:
        model = Proyecto
        fields = ('lider',)


class RolSistemaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RolSistemaForm, self).__init__(*args, **kwargs)
        self.fields['permisos'].queryset = Permiso.objects.filter(tipo="SISTEMA")
        for field in self.fields:
            self.fields[field].error_messages = {'required':'Este campo es obligatorio'}
    class Meta:
        model= Rol
        fields = ("nombre","descripcion","permisos")


class RolProyectoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RolProyectoForm, self).__init__(*args, **kwargs)
        self.fields['permisos'].queryset = Permiso.objects.filter(tipo="PROYECTO")
        for field in self.fields:
            self.fields[field].error_messages = {'required':'Este campo es obligatorio'}
    class Meta:
        model= Rol
        fields = ("nombre","descripcion","permisos")


User.add_to_class('roles', models.ManyToManyField(Rol, blank=True), )

class UsuarioFormModificar(ModelForm):

    permisos = Permiso
    class Meta:
        model = User
        fields=("username","email","first_name", "last_name","direccion", "telefono")


class UsuarioFormCambioEstado(ModelForm):

    class Meta:
        model = User
        fields=("is_active",)



class UsuarioFormAsignarRolSistema(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioFormAsignarRolSistema, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = Rol.objects.filter(tipo = 'SISTEMA')
    class Meta:
        model = User
        fields=("roles",)


class UsuarioFormAsignarCliente(ModelForm):
    class Meta:
        model = User
        fields=("cliente",)


class ClienteForm(forms.ModelForm):
    class Meta:
        model= Cliente
        fields = ("nombre","direccion","telefono","observacion","correo")


class ClienteFormCambioEstado(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ("estado",)




class Equipo(models.Model):
    usuario = models.ForeignKey(User, related_name='usuarioequipo')
    proyecto = models.ForeignKey(Proyecto, related_name='proyectoequipo',null=True)
    rol = models.ForeignKey(Rol, related_name='rolequipo', null=True)
    hora = models.IntegerField(default=1)

    def __unicode__(self):
        return self.usuario.username


class EquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipoForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.filter(tipo="PROYECTO")
        self.fields['usuario'].queryset = User.objects.all().exclude(cliente__in = Cliente.objects.all())
        for field in self.fields:
            self.fields[field].error_messages = {'required':'Este campo es obligatorio'}
    class Meta:
        model = Equipo
        fields = ("usuario","hora","rol")


class EquipoRolForm(ModelForm):

    class Meta:
        model= Equipo
        fields = ('rol',)










class Files (models.Model):
    nombre = models.CharField(max_length=60)
    dato   =models.BinaryField()
    def __unicode__(self):
        return self.nombre


class Trabajo(models.Model):
    def obtener_nombre_archivo(instance, filename):
        return "Archivos subidos/%s_%s" % (str(time()).replace('.'',''_'),filename)
    nombre = models.CharField(max_length=60)
    horas = models.PositiveIntegerField(default=0)
    fecha = models.CharField(max_length=60)
    nota = models.TextField(max_length=200)
    actor = models.CharField(max_length=60)
    archivo = models.OneToOneField(Files,related_name='archivo', null=True)
#    hu = models.ForeignKey(Hu, related_name='historiatrabajo', null=False)
    filename = models.CharField(max_length=60, null=True)
    size = models.IntegerField(null=True)
    flujo = models.CharField(max_length=60, null=True)
    actividad = models.CharField(max_length=60, null=True)
    estado = models.CharField(max_length=60, null=True)
    sprint = models.CharField(max_length=60, null=True)

    def __unicode__(self):
        return self.nombre

class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ("nombre","horas","nota")

