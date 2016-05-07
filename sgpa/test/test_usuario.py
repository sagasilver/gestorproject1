
import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
class GTGTestCase(TestCase):

   def test_crear_usuario(self):
        '''
        Test para la creacion de un usuario con contrasenha
        '''
        print('\n------Ejecutando test para crear usuario-------\n')

        u = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        self.assertTrue(u.has_usable_password())
        self.assertFalse(u.check_password('bad'))
        self.assertTrue(u.check_password('testpw'))
        print('\n------Test para crear usuario correcto-------\n')

        print('\n------Ejecutando test para contrasenha incorrecta-------\n')
        # Test para contrasenha incorrecta
        u.set_unusable_password()
        u.save()
        self.assertFalse(u.check_password('testpw'))
        self.assertFalse(u.has_usable_password())
        u.set_password('testpw')
        self.assertTrue(u.check_password('testpw'))
        u.set_password(None)
        self.assertFalse(u.has_usable_password())
        print('\n------Test para crear contrasenha incorrecta correcto-------\n')

        print('\n------Ejecutando test para identificar permiso-------\n')
        # Test para identificar permisos
        self.assertTrue(u.is_authenticated())
        self.assertFalse(u.is_staff)
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_superuser)
        print('\n------Test para identificar permiso correcto-------\n')

        def test_eliminar_usuario(self):
	    '''
	    Test para la eliminacion de un usuario
	    '''
        print('\n------Ejecutando test para eliminar usuario-------\n')
        u = User.objects.create_user('testuser33', 'test@example.com', 'testpw')
        a = User.objects.get(pk=u.id)
        self.assertNumQueries(7, a.delete)
        self.assertTrue(User.objects.exists())
        print('\n------Test para eliminar usuario correcto-------\n')

        # Test para creacion sin password
        u2 = User.objects.create_user('testuser2', 'test2@example.com')
        self.assertFalse(u2.has_usable_password())
def test_inicio(self):
    '''
                Test para ver si puede entrar a la pagina de inicio
    '''

    def test_modificar_usuarios(self):
        '''
        Test para modificar un usuario
        '''
        print('\n------Ejecutando test para modificar usuario...-------\n')

        usuario2 = User.objects.create_user('testuser33', 'test@example.com', 'testpw')
        usuario2.is_active=False
        resp = self.client.get('/usuario/modificar_usuario/1?')
        self.assertEqual(resp.status_code, 301)

        self.assertEqual([usuario2.is_active for user in resp.context['datos']], [False])
        print('\n------Test de modificar usuario exitoso-------\n')

    def logout(self):
        '''
        Test para el logout
        '''
        print('\n------Ejecutando test para logout-------\n')

        response = self.client.get('/cerrar/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)
        print('\n------Test para logout exitoso-------\n')

