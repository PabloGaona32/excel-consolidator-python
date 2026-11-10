import pandas as pd

def estandarizar_columnas(df):
    if not df.empty:
        df.columns = df.columns.astype(str).str.strip()
    return df

def verificar_columnas_obligatorias(df, columnas_obligatorias, nombre_archivo, nombre_hoja, registro_errores):
    """Verifica que no falte ninguna columna requerida."""
    if not df.empty:
        faltantes = [col for col in columnas_obligatorias if col not in df.columns]
        if faltantes:
            registro_errores.append({
                "Archivo": nombre_archivo,
                "Hoja": nombre_hoja,
                "Problema": f"Faltan columnas obligatorias: {', '.join(faltantes)}"
            })
    return registro_errores

def limpiar_datos_numericos(df, columnas_numericas, nombre_archivo, nombre_hoja, registro_errores):
    for col in columnas_numericas:
        if col in df.columns:
            estaba_vacio = df[col].isna() | (df[col].astype(str).str.strip() == "")
            
            # AJUSTE MXN: Regex que deja ÚNICAMENTE dígitos, punto y signo menos.
            # Borrará comas, signos de pesos y letras (MXN) de un plumazo.
            limpios = df[col].astype(str)
            limpios = limpios.str.replace(r'[^\d\.-]', '', regex=True)
            
            # Convertimos. Las palabras completas ("Sin stock") quedarán como NaN (vacías).
            convertidos = pd.to_numeric(limpios, errors='coerce')
            
            fallaron = (~estaba_vacio) & convertidos.isna()
            
            if fallaron.any():
                filas_excel = (fallaron[fallaron].index + 2).tolist()
                
                # AJUSTE REVISIÓN: Conteo y muestra corta en lugar de lista infinita
                total = len(filas_excel)
                ejemplos = filas_excel[:5] 
                
                registro_errores.append({
                    "Archivo": nombre_archivo,
                    "Hoja": nombre_hoja,
                    "Problema": f"Texto inválido en '{col}'. {total} fila(s) afectadas (ej. {ejemplos}). Se dejaron vacías."
                })
            
            df[col] = convertidos
                
    return df, registro_errores