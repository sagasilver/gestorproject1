
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_modificar_cliente(self):
	
	        c = Client()
	        c.login(username='gustavo', password='gustavo')
		print('\n------Ejecutando test para modificar un cliente-------\n')

	        resp = c.get('/usuario/cliente/1')
	        self.assertTrue(resp.status_code, 200)
