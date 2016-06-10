
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client

class SGPATestCase(TestCase):
	def test_ver_hu(self):

	        c = Client()
	        c.login(username='gustavo', password='gustavo')
		print('\n------Ejecutando test para ver HU-------\n')

	        resp = c.get('/usuario/ver_hu/1')
	        self.assertTrue(resp.status_code, 200)