
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_visualizar_proyecto(self):
        

	        c = Client()
	        c.login(username='gustavo', password='123')
	        print('\n------Ejecutando test para ver detalle  proyecto...-------')
	
	        resp = c.get('http://127.0.0.1:8000/usuario/detalle_proyecto/1/')
	        self.assertEqual(resp.status_code, 302)
