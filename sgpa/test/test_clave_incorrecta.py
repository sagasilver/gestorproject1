
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_clave_incorrecta(self):
		print('\n------Ejecutando test para contrasenha incorrecta-------\n')
        	# Test para contrasenha incorrecta
		u = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        	u.set_unusable_password()
        	u.save()
        	self.assertFalse(u.check_password('testpw'))
        	self.assertFalse(u.has_usable_password())
        	u.set_password('testpw')
        	self.assertTrue(u.check_password('testpw'))
        	u.set_password(None)
        	self.assertFalse(u.has_usable_password())
