
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_identificar_permiso(self):
		print('\n------Ejecutando test para identificar permiso-------\n')
        	# Test para identificar permisos
		u = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        	self.assertTrue(u.is_authenticated())
        	self.assertFalse(u.is_staff)
        	self.assertTrue(u.is_active)
        	self.assertFalse(u.is_superuser)
