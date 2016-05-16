
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class SGPATestCase(TestCase):
	def test_eliminar_usuario(self):
	    	'''
	    	Test para la eliminacion de un usuario
	    	'''
        	print('\n------Ejecutando test para eliminar usuario-------\n')
        	u = User.objects.create_user('testuser33', 'test@example.com', 'testpw')
        	a = User.objects.get(pk=u.id)
        	self.assertNumQueries(8, a.delete)
        	self.assertFalse(User.objects.exists())
