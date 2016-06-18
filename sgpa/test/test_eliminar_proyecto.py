
from django.test import TestCase
from sgpa.models import Proyecto, Cliente



class SGPATestCase(TestCase):
	def test_eliminar_proyecto(self):

         print('\n------Ejecutando test para eliminar proyecto...-------')
         c = Cliente(nombre= 'cliente', correo='asd@ejemplo.com')
         c.save()
         p = Proyecto(fechaInicio= '12-05-2016', fechaFin='20-06-2016',nombre = 'proyecto', cliente= 'cliente')
         p.save()
         c = Proyecto.objects.get(pk = p.id)
         c.delete()
         self.assertFalse(Proyecto.objects.exists())
