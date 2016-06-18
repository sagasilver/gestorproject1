
from django.test import TestCase
from sgpa.models import Cliente



class SGPATestCase(TestCase):
	def test_eliminar_cliente(self):
         print('\n------Ejecutando test para eliminar cliente-------\n')
         c = Cliente(nombre= 'cliente', correo='asd@ejemplo.com')
         c.save()
         a = Cliente.objects.get(pk = c.id)
         a.delete()
         self.assertFalse(Cliente.objects.exists())


