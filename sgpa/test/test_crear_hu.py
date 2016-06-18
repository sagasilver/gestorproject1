
from django.test import TestCase
from sgpa.models import Hu



class SGPATestCase(TestCase):
	def test_crear_hu(self):

         print('\n------Ejecutando test para crear hu...-------')
         hu = Hu(nombre = 'hola', observacion= 'sdfdf')
         hu.save()
         self.assertTrue(Hu.objects.exists())
