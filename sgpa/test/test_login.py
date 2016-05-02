from unittest import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY

__author__ = 'luis'

class TestInicio_sesion(TestCase):
    def setUp(self):

        """Test para las pruebas unitarias.
         Inicio sesion
         import: importa los modulos necesarios
        """
        self.client = Client()
        self.username = 'trtr'
        self.email = 'test@tesm'
        self.password = 'stpw'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
        print('\n------Ejecutando test para inicio de sesion...-------\n')


    def test_inicio_sesion_exitoso(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)
        print('\n------Test de inicio de inicio de sesion exitoso-------\n')

	
   
