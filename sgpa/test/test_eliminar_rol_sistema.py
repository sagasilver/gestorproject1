
from django.test import TestCase
from sgpa.models import Rol


class SGPATestCase(TestCase):
	def test_eliminar_Rol_Sistema(self):
	


		print('\n------Ejecutando test para eliminar Rol Sistema-------\n')
	        r = Rol(nombre='ejemploRol', descripcion='Rol de Sistema')
                r.save()
	        a = Rol.objects.get(pk = r.id)
                a.delete()

	        self.assertFalse(Rol.objects.exists())
