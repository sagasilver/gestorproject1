
from django.test import TestCase
from sgpa.models import Sprint



class SGPATestCase(TestCase):
	def test_activar_sprint(self):

         print('\n------Ejecutando test para activar sprint...-------')
         s = Sprint(duracion = 1, fechaInicio= '01-12-2016', fechaFin='12-12-2016', nombre='sprint', estado = 'INA')
         s.save()
         s.estado= 'ACT'
         s.save()
         self.assertEqual(s.estado,'ACT')
