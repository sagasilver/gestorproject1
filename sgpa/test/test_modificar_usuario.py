
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_modificar_usuarios(self):
        	'''
        	Test para modificar un usuario
        	'''
        	print('\n------Ejecutando test para modificar usuario...-------\n')

        	usuario1 = User.objects.create_user('pepe', 'test@example.com', 'abc')
                usuario2 = User.objects.create_user('lalo', 'test@example.com', 'deg')
                usuario2.email = 'modificado@example.com'
                usuario2.save()
        	self.assertNotEqual(usuario2.email,usuario1.email)
