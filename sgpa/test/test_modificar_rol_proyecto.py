
from django.test import TestCase
from sgpa.models import Rol

class SGPATestCase(TestCase):
	def test_modificar_rol_proyecto(self):
        	'''
        	Test para modificar rol de proyecto
        	'''
        	print('\n------Ejecutando test para modificar rol de proyecto...-------\n')

        	rol1 = Rol(nombre='Rol1', descripcion='Rol de Proyecto')
                rol2 = Rol(nombre='Rol2', descripcion='Rol de Sistema')
                rol2.descripcion = 'Rol modificado'
                rol2.save()
        	self.assertNotEqual(rol1.descripcion,rol2.descripcion)