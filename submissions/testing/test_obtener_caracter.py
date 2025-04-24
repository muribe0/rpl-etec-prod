import unittest

class Test(unittest.TestCase):
    def test_esta_definida(self):
        self.assertIn('foo', globals(), "La función no está definida")

    def test_es_una_funcion(self):
        self.assertTrue(callable(foo), "No es una función callable")
        self.assertEqual(type(foo), type(lambda x: x), "No es una función")

    def test_parametros(self):
        try:
            self.assertEqual(foo.__code__.co_argcount, 2,
                             "La función debe recibir 2 parámetro")
        except AttributeError:
            self.fail("La función no tiene la estructura correcta")

    def test_cadena_comienza_con_espacio(self):
        resultado = foo(" Hola", 0)

        self.assertIsInstance(resultado, str,
                              "El resultado debe ser una cadena")
        self.assertEqual(resultado, " ",
                         "Debe retornar un espacio si la cadena comienza con un espacio y la posicion es 0")

    def test_retorna_primer_letra(self):
        try:
            resultado = foo("Patroclo", 0)
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
