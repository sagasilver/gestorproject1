
from django.test import TestCase
from sgpa.models import Cliente



class SGPATestCase(TestCase):
	def test_modificar_cliente(self):

         print('\n------Ejecutando test para modificar Cliente...-------')
         c1 = Cliente(nombre= 'cliente1', correo='prueba@ejemplo.com')
         c2 = Cliente(nombre= 'cliente2', correo='prueba@ejemplo.com')
         c2.correo = 'modificado@ejemplo.com'
         c2.save()
         self.assertNotEqual(c1.correo, c2.correo)
