import pandas as pd

def generar_datos_resumen(maestra, duplicados_eliminados, filas_leidas, columnas_a_sumar):
    """
    Toma la tabla maestra consolidada y calcula la contabilidad final:
    Totales de filas, qué aportó cada archivo, y la suma de las columnas numéricas.
    """
    filas_finales = len(maestra)
    cantidad_duplicados = len(duplicados_eliminados)
    
    # 1. Creamos la primera parte del resumen: La contabilidad de filas (como una tabla pequeña)
    metricas = {
        "Métrica": [
            "Total de filas leídas de origen",
            "Filas duplicadas eliminadas",
            "Total de filas en hoja Maestra final"
        ],
        "Cantidad": [
            filas_leidas,
            cantidad_duplicados,
            filas_finales
        ]
    }
    df_metricas = pd.DataFrame(metricas)
    
    # 2. Resumen por archivo: ¿Cuántas filas finales aportó cada Excel?
    if not maestra.empty:
        # value_counts cuenta cuántas veces aparece cada 'archivo_origen'
        df_por_archivo = maestra["archivo_origen"].value_counts().reset_index()
        df_por_archivo.columns = ["Archivo Origen", "Filas Aportadas (Finales)"]
    else:
        df_por_archivo = pd.DataFrame(columns=["Archivo Origen", "Filas Aportadas (Finales)"])
        
    # 3. Suma de columnas numéricas (Solo si las columnas existen en la hoja maestra)
    sumas = {"Columna": [], "Suma Total": []}
    if not maestra.empty:
        for col in columnas_a_sumar:
            if col in maestra.columns:
                # Sumamos omitiendo los valores vacíos (NaN)
                total = maestra[col].sum(skipna=True)
                sumas["Columna"].append(col)
                sumas["Suma Total"].append(total)
            else:
                sumas["Columna"].append(col)
                sumas["Suma Total"].append("Columna no encontrada en los datos")
                
    df_sumas = pd.DataFrame(sumas)
    
    return df_metricas, df_por_archivo, df_sumas