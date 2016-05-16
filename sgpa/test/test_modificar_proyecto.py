
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_modificar_proyecto(self):
	        '''
	        test para comprobar que se crea un item hijo
	        '''

	        c = Client()
	        c.login(username='gustavo', password='gustavo')
		print('\n------Ejecutando test para modificar proyecto...-------')
		resp = c.post('/usuario/modificar_proyecto/1/',{'nombre':'sgpa'})
	        self.assertTrue(resp.status_code,200)
