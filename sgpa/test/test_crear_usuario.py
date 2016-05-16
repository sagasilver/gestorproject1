
import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
class SGPATestCase(TestCase):
	def test_crear_usuario(self):
        	'''
        	Test para la creacion de un usuario con contrasenha
        	'''
        	print('\n------Ejecutando test para crear usuario-------\n')

        	u = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        	self.assertTrue(u.has_usable_password())
        	self.assertFalse(u.check_password('bad'))
        	self.assertTrue(u.check_password('testpw'))
