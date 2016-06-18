
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_desplegar_kanban(self):
	
	        c = Client()
	        c.login(username='gustavo', password='123')
		print('\n------Ejecutando test para desplegar kanban-------\n')

	        resp = c.get('/usuario/desplegar_kanban/1')
	        self.assertTrue(resp.status_code, 300)
