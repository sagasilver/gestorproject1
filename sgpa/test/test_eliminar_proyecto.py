
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_eliminar_proyecto(self):
	
	        c = Client()
	        c.login(username='gustavo', password='gustavo')
	        print('\n------Ejecutando test para eliminar proyecto-------\n')
	        resp = c.get('/usuario/eliminar_proyecto/1')
	        self.assertEqual(resp.status_code, 301)
