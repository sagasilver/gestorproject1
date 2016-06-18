
import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
class GTGTestCase(TestCase):
    

    def logout(self):
        '''
        Test para el logout
        '''
        print('\n------Ejecutando test para logout-------\n')

        response = self.client.get('/usuario/cerrar_sesion')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)
        print('\n------Test para logout exitoso-------\n')

