
from django.test import TestCase
from django.contrib.auth.models import User
class SGPATestCase(TestCase):
	def test_eliminar_usuario(self):
	    	'''
	    	Test para la eliminacion de un usuario
	    	'''
        	print('\n------Ejecutando test para eliminar usuario-------\n')
        	u = User.objects.create_user('testuser33', 'test@example.com', 'testpw')
        	a = User.objects.get(pk=u.id)
        	a.delete()
        	self.assertFalse(User.objects.exists())
