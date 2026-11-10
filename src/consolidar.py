import pandas as pd
from src.validar import estandarizar_columnas, limpiar_datos_numericos, verificar_columnas_obligatorias

def consolidar_datos(lista_dataframes, columnas_a_sumar, columnas_obligatorias, quitar_duplicados, registro_errores):
    if not lista_dataframes:
        return pd.DataFrame(), pd.DataFrame(), 0, registro_errores
        
    dfs_limpios = []
    filas_totales_leidas = 0
    
    for df in lista_dataframes:
        filas_totales_leidas += len(df)
        df = estandarizar_columnas(df)
        
        nombre_archivo = df["archivo_origen"].iloc[0]
        nombre_hoja = df["hoja_origen"].iloc[0]
        
        # AJUSTE: Ejecutar revisión de columnas faltantes
        registro_errores = verificar_columnas_obligatorias(
            df, columnas_obligatorias, nombre_archivo, nombre_hoja, registro_errores
        )
        
        df, registro_errores = limpiar_datos_numericos(
            df, columnas_a_sumar, nombre_archivo, nombre_hoja, registro_errores
        )
        
        dfs_limpios.append(df)
        
    maestra = pd.concat(dfs_limpios, ignore_index=True)
    duplicados_eliminados = pd.DataFrame()
    
    if quitar_duplicados:
        columnas_originales = [col for col in maestra.columns if col not in ["archivo_origen", "hoja_origen"]]
        es_duplicado = maestra.duplicated(subset=columnas_originales, keep='first')
        duplicados_eliminados = maestra[es_duplicado].copy()
        maestra = maestra[~es_duplicado].copy()
        
    return maestra, duplicados_eliminados, filas_totales_leidas, registro_errores