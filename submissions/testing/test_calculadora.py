import unittest

class Test(unittest.TestCase):
    """
    Test para la funcion foo
    """

    """ ===== TEST COMUNES ===== """
    def test_esta_definida(self):
        self.assertIn('foo', globals(), "La función no está definida")

    def test_es_una_funcion(self):
        self.assertTrue(callable(foo), "No es una función callable")
        self.assertEqual(type(foo), type(lambda x: x), "No es una función")

    def test_parametros(self):
        cantidad = 3
        try:
            self.assertEqual(foo.__code__.co_argcount, cantidad,
                             f"La función suma debe recibir {cantidad} parámetros")
        except AttributeError:
            self.fail("La función no tiene la estructura correcta")

    def test_retorna_valor(self):
        try:
            resultado = foo(1, 2, '+')
        except TypeError:
            self.fail("Error al ejecutar la función")

        self.assertIsNotNone(resultado,
                             "La función no retorna un valor")

    """ ===== TEST ESPECIFICOS ===== """

    def test_suma(self):
        try:
            resultado = foo(1, 2, '+')
        except TypeError:
            self.fail("La función no acepta enteros como parámetros")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un entero")
        self.assertEqual(resultado, 3,
                         "La suma de 1 y 2 debe ser 3")

    def test_suma_negativos(self):
        try:
            resultado = foo(-1, -2, '+')
        except TypeError:
            self.fail("La función no acepta enteros negativos como parámetros")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un entero")
        self.assertEqual(resultado, -3,
                         "La suma de -1 y -2 debe ser -3")

    def test_suma_floats(self):
        try:
            resultado = foo(1.5, 2.5, '+')
        except TypeError:
            self.fail("La función no acepta flotantes como parámetros")

        self.assertIsInstance(resultado, float,
                              "El resultado debe ser un float")
        self.assertEqual(resultado, 4.0,
                         "La suma de 1.5 y 2.5 debe ser 4.0")

    def test_resta(self):
        try:
            resultado = foo(5, 3, '-')
        except TypeError:
            self.fail("La función no acepta enteros como parámetros")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un entero")
        self.assertEqual(resultado, 2,
                         "La resta de 5 y 3 debe ser 2")

    def test_multiplicacion(self):
        try:
            resultado = foo(2, 3, '*')
        except TypeError:
            self.fail("La función no acepta enteros como parámetros")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un entero")
        self.assertEqual(resultado, 6,
                         "La multiplicación de 2 y 3 debe ser 6")

    def test_division(self):
        try:
            resultado = foo(6, 3, '/')
        except TypeError:
            self.fail("La función no acepta enteros como parámetros")

        self.assertIsInstance(resultado, float,
                              "El resultado debe ser un float")
        self.assertEqual(resultado, 2.0,
                         "La división de 6 y 3 debe ser 2.0")



if __name__ == '__main__':
    unittest.main()