
from django.test import TestCase
from sgpa.models import Rol


class SGPATestCase(TestCase):
	def test_eliminar_Rol_Proyecto(self):
	


		print('\n------Ejecutando test para eliminar Rol Proyecto-------\n')
	        r = Rol(nombre='ejemploRol', descripcion='Rol de Proyecto')
                r.save()
	        a = Rol.objects.get(pk = r.id)
                a.delete()

	        self.assertFalse(Rol.objects.exists())
