import unittest

class Test(unittest.TestCase):
    def test_esta_definida(self):
        self.assertIn('foo', globals(), "La función no está definida")

    def test_es_una_funcion(self):
        self.assertTrue(callable(foo), "No es una función callable")
        self.assertEqual(type(foo), type(lambda x: x), "No es una función")

    def test_parametros(self):
        try:
            self.assertEqual(foo.__code__.co_argcount, 1,
                             "La función debe recibir 1 parámetro")
        except AttributeError:
            self.fail("La función no tiene la estructura correcta")

    def test_cadena_no_tiene_vocales(self):
        resultado = foo("jlktrvvtrknlrtlnvgtrbkhv")

        self.assertIsInstance(resultado, int,
                              "El resultado debe ser un numero entero")
        self.assertEqual(resultado, 0,
                         "Debe retornar 0 si la cadena no tiene vocales")

    def test_cadena_solo_tiene_vocales_mayusculas(self):
        try:
            resultado = foo("AEIOU", 0)
        except TypeError:
            self.fail("Error al ejecutar la función")

        self.assertIsNotNone(resultado,
                             "La función no retorna un valor")
        self.assertEqual(resultado, "P",
                 "Debe retornar la P si la cadena es Patroclo")

    def test_retorna_ultima_letra(self):
        cadena = "Patroclo"
        try:
            resultado = foo(cadena, len(cadena) - 1)
        except TypeError:
            self.fail("Error al ejecutar la función")

        self.assertIsNotNone(resultado,
                             "La función no retorna un valor")
        self.assertEqual(resultado, "o",
                         f"Debe retornar la o si la cadena es Patroclo y la posicion es {len(cadena)-1} (último caracter)")


if __name__ == '__main__':
    unittest.main()
