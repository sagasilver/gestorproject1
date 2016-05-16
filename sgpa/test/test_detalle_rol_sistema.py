
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_detalle_Rol_Sistema(self):
	
	        c = Client()
	        c.login(username='gustavo', password='gustavo')
		print('\n------Ejecutando test para ver detalle Rol Sistema-------\n')

	        resp = c.get('/usuario/detalle_rol_sistema/1')
	        self.assertTrue(resp.status_code, 200)
