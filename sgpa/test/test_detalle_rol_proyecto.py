
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_ver_Rol_Proyecto(self):
	
	        c = Client()
	        c.login(username='gustavo', password='gustavo')
		print('\n------Ejecutando test para ver Rol Proyecto-------\n')

	        resp = c.get('/usuario/ver_rol_proyecto/1')
	        self.assertTrue(resp.status_code, 200)
