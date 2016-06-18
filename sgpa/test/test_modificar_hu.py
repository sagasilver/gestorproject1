
from django.test import TestCase
from sgpa.models import Hu



class SGPATestCase(TestCase):
	def test_modificar_hu(self):

         print('\n------Ejecutando test para modificar Hu...-------')
         hu1 = Hu(nombre = 'userhistory1', observacion= 'observacion')
         hu2 = Hu(nombre = 'userhistory2', observacion= 'observacion')
         hu2.observacion = 'observacion modificado'
         hu2.save()
         self.assertNotEqual(hu1.observacion, hu2.observacion)
