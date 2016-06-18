
from django.test import TestCase
from sgpa.models import Hu



class SGPATestCase(TestCase):
	def test_eliminar_hu(self):

         print('\n------Ejecutando test para eliminar hu...-------')
         hu = Hu(nombre = 'userhistory', observacion= 'sdfdf')
         hu.save()
         a = Hu.objects.get(pk = hu.id)
         a.delete()
         self.assertFalse(Hu.objects.exists())
