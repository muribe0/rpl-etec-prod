import unittest

class TestSuma(unittest.TestCase):
    def test_esta_definida(self):
        self.assertIn('foo', globals(), "La función no está definida")

    def test_es_una_funcion(self):
        self.assertTrue(callable(foo), "No es una función callable")
        self.assertEqual(type(foo), type(lambda x: x), "No es una función")

    def test_parametros(self):
        try:
            self.assertEqual(foo.__code__.co_argcount, 2,
                             "La función suma debe recibir dos parámetros")
        except AttributeError:
            self.fail("La función no tiene la estructura correcta")

    def test_suma_enteros(self):
        try:
            resultado = foo(1, 2)
        except TypeError:
            self.fail("La función no acepta enteros como parámetros")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un entero")
        self.assertEqual(resultado, 3,
                         "La suma de 1 y 2 debe ser 3")

    def test_suma_negativos(self):
        try:
            resultado = foo(-1, -2)
        except TypeError:
            self.fail("La función no acepta enteros negativos como parámetros")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un entero")
        self.assertEqual(resultado, -3,
                         "La suma de -1 y -2 debe ser -3")

    def test_suma_floats(self):
        try:
            resultado = foo(1.5, 2.5)
        except TypeError:
            self.fail("La función no acepta flotantes como parámetros")

        self.assertIsInstance(resultado, float,
                              "El resultado debe ser un float")
        self.assertEqual(resultado, 4.0,
                         "La suma de 1.5 y 2.5 debe ser 4.0")

    def test_retorna_valor(self):
        try:
            resultado = foo(1, 2)
        except TypeError:
            self.fail("Error al ejecutar la función")

        self.assertIsNotNone(resultado,
                             "La función no retorna un valor")


if __name__ == '__main__':
    unittest.main()