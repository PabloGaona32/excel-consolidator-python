import sys
import os
from datetime import datetime
from config import CARPETA_ENTRADA, CARPETA_SALIDA, CARPETA_LOGS, ARCHIVO_SALIDA, QUITAR_DUPLICADOS, COLUMNAS_A_SUMAR, COLUMNAS_OBLIGATORIAS

from src.leer_archivos import obtener_archivos_validos, procesar_archivos
from src.consolidar import consolidar_datos
from src.resumen import generar_datos_resumen
from src.exportar import guardar_excel_final

def crear_log(archivos, archivos_ignorados, filas_leidas, filas_finales, duplicados, errores, maestra, estado):
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta_log = os.path.join(CARPETA_LOGS, f"ejecucion_{fecha}.txt")
    
    with open(ruta_log, "w", encoding="utf-8") as f:
        f.write(f"=== LOG DE EJECUCIÓN - {fecha} ===\n")
        f.write(f"ESTADO: {estado}\n")
        
        if estado == "ÉXITO":
            f.write(f"Archivo generado en: {os.path.abspath(ARCHIVO_SALIDA)}\n")
        else:
            f.write("Archivo Excel NO generado debido a errores críticos.\n")
            
        f.write("\n--- ARCHIVOS ---\n")
        f.write(f"Procesados (.xlsx): {len(archivos)}\n")
        f.write(f"Ignorados (temporales/otros): {len(archivos_ignorados)}\n")
        if archivos_ignorados:
            f.write(f" Lista de ignorados: {', '.join(archivos_ignorados)}\n")
            
        f.write("\n--- CONTABILIDAD DE FILAS ---\n")
        f.write(f"Filas leídas originales : {filas_leidas}\n")
        f.write(f"Filas finales en maestra: {filas_finales}\n")
        f.write(f"Duplicados eliminados   : {duplicados}\n")
        
        f.write("\n--- SUMAS DE COLUMNAS NUMÉRICAS ---\n")
        if maestra is not None and not maestra.empty:
            for col in COLUMNAS_A_SUMAR:
                if col in maestra.columns:
                    total = maestra[col].sum(skipna=True)
                    # AJUSTE 2: Etiqueta dinámica si los datos están corruptos
                    advertencia = "" if estado == "ÉXITO" else " (no confiables)"
                    f.write(f"{col}: {total:,.2f}{advertencia}\n")
                else:
                    f.write(f"{col}: Columna no encontrada\n")
        else:
            f.write("No hay datos consolidados para sumar.\n")
        
        f.write("\n--- DETALLE DE ALERTAS / ERRORES ---\n")
        f.write(f"Total de alertas: {len(errores)}\n")
        for e in errores:
            f.write(f"[{e.get('Archivo', 'General')} | {e.get('Hoja', 'N/A')}] {e.get('Problema', '')}\n")
            
    print(f"Log guardado en: {ruta_log}")

def ejecutar_proceso():
    print("=== INICIANDO CONSOLIDADOR DE EXCEL ===")
    
    # AJUSTE 1: Prevenir falsos positivos borrando el reporte anterior
    if os.path.exists(ARCHIVO_SALIDA):
        try:
            os.remove(ARCHIVO_SALIDA)
            print("[INFO] Archivo de salida anterior eliminado para evitar confusiones.")
        except PermissionError:
            # Beneficio extra: atrapamos si el usuario dejó el Excel viejo abierto
            print(f"\n[ERROR CRÍTICO] No se puede borrar '{ARCHIVO_SALIDA}'.")
            print("¿Lo tienes abierto en Excel? Ciérralo e intenta ejecutar de nuevo.")
            sys.exit(1)
        except Exception as e:
            print(f"\n[ERROR CRÍTICO] Fallo al borrar el archivo anterior: {e}")
            sys.exit(1)
            
    rutas_archivos, archivos_ignorados = obtener_archivos_validos(CARPETA_ENTRADA)
    
    if not rutas_archivos:
        print("[ADVERTENCIA] No se encontraron archivos.")
        crear_log([], archivos_ignorados, 0, 0, 0, [{"Problema": "Sin archivos .xlsx para procesar"}], None, "ADVERTENCIA - SIN DATOS")
        sys.exit(0)
        
    lista_dataframes, registro_errores = procesar_archivos(rutas_archivos)
    
    maestra, duplicados_eliminados, filas_leidas, registro_errores = consolidar_datos(
        lista_dataframes, COLUMNAS_A_SUMAR, COLUMNAS_OBLIGATORIAS, QUITAR_DUPLICADOS, registro_errores
    )
    
    filas_finales = len(maestra) + 1
    cantidad_duplicados = len(duplicados_eliminados)
    
    if (filas_finales + cantidad_duplicados) != filas_leidas:
        print("\n[ERROR CRÍTICO] La contabilidad de filas no cuadra.")
        
        registro_errores.append({
            "Archivo": "SISTEMA", 
            "Hoja": "VERIFICACIÓN", 
            "Problema": f"Descuadre matemático. Leídas ({filas_leidas}) != Finales ({filas_finales}) + Duplicados ({cantidad_duplicados})"
        })
        
        crear_log(rutas_archivos, archivos_ignorados, filas_leidas, filas_finales, cantidad_duplicados, registro_errores, maestra, "ERROR CRÍTICO")
        sys.exit(1)
    
    df_metricas, df_por_archivo, df_sumas = generar_datos_resumen(
        maestra, duplicados_eliminados, filas_leidas, COLUMNAS_A_SUMAR
    )
    
    guardar_excel_final(
        maestra, duplicados_eliminados, registro_errores,
        df_metricas, df_por_archivo, df_sumas, ARCHIVO_SALIDA
    )
    
    crear_log(rutas_archivos, archivos_ignorados, filas_leidas, filas_finales, cantidad_duplicados, registro_errores, maestra, "ÉXITO")
    print("=== PROCESO TERMINADO CON ÉXITO ===")

if __name__ == "__main__":
    ejecutar_proceso()