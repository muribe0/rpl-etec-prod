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
                             "La función debe recibir dos parámetros")
        except AttributeError:
            self.fail("La función no tiene la estructura correcta")

    def test_cadenas_vacias(self):
        try:
            resultado = foo("", "")
        except TypeError:
            self.fail("La funcion no acepta strings como parametros")

        self.assertIsInstance(resultado, str,
                              "El resultado debe ser una cadena")
        self.assertEqual(resultado, "",
                         'Concatenar nombre="" apellido="" debe ser ""')

    def test_nombre_apellido(self):
        resultado = foo("Cosme", "Fulanito")

        self.assertIsInstance(resultado, str,
                              "El resultado debe ser una cadena")
        self.assertEqual(resultado, "Coseme Fulanito",
                         "Cosme Fulanito")

    def test_retorna_valor(self):
        try:
            resultado = foo("", "")
        except TypeError:
            self.fail("Error al ejecutar la función")

        self.assertIsNotNone(resultado,
                             "La función no retorna un valor")


if __name__ == '__main__':
    unittest.main()
