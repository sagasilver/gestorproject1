
from django.test import TestCase
from sgpa.models import Proyecto, Cliente



class SGPATestCase(TestCase):
	def test_modificar_proyecto(self):

         print('\n------Ejecutando test para modificar proyecto...-------')
         c = Cliente(nombre= 'cliente', correo='asd@ejemplo.com')
         c.save()
         p1 = Proyecto(fechaInicio= '12-05-2016', fechaFin='20-06-2016',nombre = 'proyecto1', cliente= 'cliente')
         p2 = Proyecto(fechaInicio= '12-05-2016', fechaFin='20-06-2016',nombre = 'proyecto2', cliente= 'cliente')
         p2.fechaInicio = '13-06-2016'
         p2.save()
         self.assertNotEqual(p1.fechaInicio, p2.fechaInicio)
