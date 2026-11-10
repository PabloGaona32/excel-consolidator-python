import os
import pandas as pd

def obtener_archivos_validos(carpeta_entrada):
    archivos_validos = []
    archivos_ignorados = [] # NUEVO: Rastrear lo que saltamos
    
    if not os.path.exists(carpeta_entrada):
        return archivos_validos, archivos_ignorados
        
    for archivo in sorted(os.listdir(carpeta_entrada)):
        ruta_completa = os.path.join(carpeta_entrada, archivo)
        
        # Ignoramos si es una carpeta
        if not os.path.isfile(ruta_completa):
            continue
            
        # Clasificamos: Válidos (.xlsx y no temporales) vs Ignorados
        if archivo.lower().endswith(".xlsx") and not archivo.startswith("~$"):
            archivos_validos.append(ruta_completa)
        else:
            archivos_ignorados.append(archivo)
            
    return archivos_validos, archivos_ignorados

def procesar_archivos(rutas_archivos):
    lista_dataframes = []
    registro_errores = []
    
    for ruta in rutas_archivos:
        nombre_archivo = os.path.basename(ruta)
        try:
            diccionario_hojas = pd.read_excel(ruta, sheet_name=None)
            if not diccionario_hojas:
                registro_errores.append({"Archivo": nombre_archivo, "Hoja": "N/A", "Problema": "El archivo no tiene hojas o está vacío."})
                continue
                
            for nombre_hoja, df in diccionario_hojas.items():
                # CORRECCIÓN: Garantizar que la hoja vacía se anote siempre.
                # len(df) == 0 cubre el caso donde Pandas lee el cascarón pero no hay datos.
                if df.empty or len(df) == 0:
                    registro_errores.append({
                        "Archivo": nombre_archivo, 
                        "Hoja": nombre_hoja, 
                        "Problema": "La hoja estaba vacía y fue ignorada."
                    })
                    continue
                    
                df["archivo_origen"] = nombre_archivo
                df["hoja_origen"] = nombre_hoja
                lista_dataframes.append(df)
        except Exception as e:
            registro_errores.append({"Archivo": nombre_archivo, "Hoja": "N/A", "Problema": f"No se pudo abrir. Error: {str(e)}"})
            
    return lista_dataframes, registro_errores