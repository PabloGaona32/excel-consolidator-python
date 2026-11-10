import unittest
import pandas as pd
from src.consolidar import consolidar_datos

class TestConsolidador(unittest.TestCase):
    def setUp(self):
        self.df1 = pd.DataFrame({" ID ": [1, 2], "Monto": [100, 200], "archivo_origen": ["a.xlsx", "a.xlsx"], "hoja_origen": ["h1", "h1"]})
        self.df2 = pd.DataFrame({"Monto": [200, 300], "ID": [2, 3], "archivo_origen": ["b.xlsx", "b.xlsx"], "hoja_origen": ["h1", "h1"]})
        self.lista_dfs = [self.df1, self.df2]
        self.columnas_sumar = ["Monto"]
        self.columnas_obligatorias = ["ID"] # Parámetro extra añadido
        self.errores = []

    def test_alineacion_y_duplicados(self):
        maestra, duplicados, filas_leidas, errores = consolidar_datos(
            self.lista_dfs, self.columnas_sumar, self.columnas_obligatorias, True, self.errores
        )
        self.assertIn("ID", maestra.columns)
        self.assertEqual(len(maestra), 3)
        self.assertEqual(filas_leidas, len(maestra) + len(duplicados))

    def test_sin_quitar_duplicados(self):
        maestra, duplicados, filas_leidas, errores = consolidar_datos(
            self.lista_dfs, self.columnas_sumar, self.columnas_obligatorias, False, self.errores
        )
        self.assertEqual(len(maestra), 4)
        self.assertEqual(filas_leidas, len(maestra) + len(duplicados))

if __name__ == "__main__":
    unittest.main()