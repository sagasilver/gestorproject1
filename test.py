
from django.test import TestCase
from sgpa.models import Cliente



class SGPATestCase(TestCase):
	def test_crear_cliente(self):
         print('\n------Ejecutando test para crear cliente-------\n')
         c = Cliente(nombre= 'cliente', correo='asd@ejemplo.com')
         c.save()
         self.assertTrue(Cliente.objects.exists())


