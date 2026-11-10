import pandas as pd
import os

def guardar_excel_final(maestra, duplicados_eliminados, registro_errores, 
                        df_metricas, df_por_archivo, df_sumas, 
                        ruta_salida):
    """
    Toma todos los DataFrames que hemos construido y los escribe en un único 
    archivo Excel con diferentes pestañas (hojas). Además, le da un poco 
    de formato básico al resumen para que sea fácil de leer.
    """
    
    # Creamos la carpeta de salida si no existe para que no lance error al intentar guardar
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # Preparamos el registro de errores para convertirlo en DataFrame
    if registro_errores:
        df_revision = pd.DataFrame(registro_errores)
    else:
        df_revision = pd.DataFrame([{"Mensaje": "Ejecución perfecta, sin errores ni advertencias."}])

    # Preparamos la hoja de duplicados
    if duplicados_eliminados.empty:
        df_duplicados = pd.DataFrame([{"Mensaje": "No se eliminaron filas duplicadas."}])
    else:
        df_duplicados = duplicados_eliminados
        
    # Usamos pd.ExcelWriter para poder escribir múltiples hojas en un solo archivo .xlsx
    with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
        
        # 1. Guardamos la tabla principal
        maestra.to_excel(writer, sheet_name='Maestra', index=False)
        
        # 2. Guardamos los duplicados por si el cliente necesita revisarlos
        df_duplicados.to_excel(writer, sheet_name='Duplicados_Eliminados', index=False)
        
        # 3. Guardamos la hoja de Revisión de errores y advertencias
        df_revision.to_excel(writer, sheet_name='Revision', index=False)
        
        # 4. Construimos la hoja de Resumen (juntando las 3 tablitas de resumen.py en una sola hoja)
        # Escribimos las métricas generales en la fila 0
        df_metricas.to_excel(writer, sheet_name='Resumen', index=False, startrow=0)
        
        # Calculamos dónde empezar a escribir la siguiente tabla (dejamos 2 filas de espacio)
        fila_archivos = len(df_metricas) + 2
        df_por_archivo.to_excel(writer, sheet_name='Resumen', index=False, startrow=fila_archivos)
        
        # Calculamos dónde empezar a escribir la última tabla
        fila_sumas = fila_archivos + len(df_por_archivo) + 2
        df_sumas.to_excel(writer, sheet_name='Resumen', index=False, startrow=fila_sumas)

    print(f"\n[ÉXITO] Archivo consolidado guardado en: {ruta_salida}")