__author__ = 'luis'
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_crear_proyecto(self):
	        '''
	        test para comprobar que se crea un item
	        '''
	
	        c = Client()
	        c.login(username='gustavo', password='gustavo')
	        print('\n------Ejecutando test para registrar un proyecto...-------\n')
	
	
	        resp = c.post('/usuario/crearproyecto',{"fechaInicio": "2014-05-07", "lider": 1, "nombre": "sgpa", "estado": "PEN", "fechaFin": "2015-05-07"})
	        self.assertTrue(resp.status_code,200)
