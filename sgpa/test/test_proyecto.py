__author__ = 'luis'
from django.test import TestCase
from django.contrib.auth.models import User
from sgpa.models import Proyecto
from django.test import Client


class GTGTestCase(TestCase):
    def test_crear_proyecto(self):
        '''
        test para comprobar que se crea un item
        '''

        c = Client()
        c.login(username='luis', password='luis')
        print('\n------Ejecutando test para registrar un proyecto...-------\n')


        resp = c.post('/usuario/crearproyecto',{"fechaInicio": "2014-05-07", "lider": 1, "nombre": "sgpa", "estado": "PEN", "fechaFin": "2015-05-07"})
        self.assertTrue(resp.status_code,200)
        print ('\n------Crea el proyecto si esta correctamente completado------git status\n')

    def test_modificar_proyecto(self):
        '''
        test para comprobar que se crea un item hijo
        '''

        c = Client()
        c.login(username='luis', password='luis')
        print('\n------Ejecutando test para modificar proyecto...-------')

        resp = c.get('/usuario/modificar_proyecto/45/')
        self.assertTrue(resp.status_code, 404)

        print ('Test acceder modificar proyecto inexistente')

        resp = c.get('/usuario/modificar_proyecto/1/')
        self.assertTrue(resp.status_code, 404)
        print ('Test acceder a modificar proyecto existente')

        resp = c.post('/usuario/modificar_proyecto/1/',{'nombre':'sgpa'})
        self.assertTrue(resp.status_code,200)
        print ('Modifica el proyecto\n')

    def test_visualizar_proyecto(self):
        '''
        test para comprobar que se crea un item hijo
        '''

        c = Client()
        c.login(username='luis', password='luis')
        print('\n------Ejecutando test para ver detalle  proyecto...-------')

        resp = c.get('/usuario/detalle_proyecto/45/')
        self.assertTrue(resp.status_code, 404)

        print ('Test acceder ver detalle proyecto inexistente')

        resp = c.get('/usuario/detalle_proyecto/1/')
        self.assertTrue(resp.status_code, 200)
        print ('Test acceder a ve detalle existente')
