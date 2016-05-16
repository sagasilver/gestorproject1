
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

        	usuario2 = User.objects.create_user('testuser33', 'test@example.com', 'testpw')
        	usuario2.is_active=False
        	resp = self.client.get('/usuario/modificar_usuario/1?')
        	self.assertEqual(resp.status_code, 301)
