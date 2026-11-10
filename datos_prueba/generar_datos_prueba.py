import pandas as pd
import os
import shutil
import random
from datetime import datetime, timedelta

CARPETA_ENTRADA = "datos_entrada"

def preparar_carpeta():
    if os.path.exists(CARPETA_ENTRADA):
        shutil.rmtree(CARPETA_ENTRADA)
    os.makedirs(CARPETA_ENTRADA)

def generar_datos_base(num_filas):
    """Genera datos realistas de ventas/inventario."""
    productos = ["Filtro de Aceite", "Balatas Delanteras", "Bujías de Iridio", 
                 "Aceite Sintético 5W-30", "Amortiguadores", "Batería 12V", "Limpiaparabrisas"]
    clientes = ["Público General", "Taller Los Compadres", "Autos GP", "Servicio Automotriz", "Flotilla ARSA"]
    
    datos = []
    fecha_base = datetime(2026, 1, 1)
    
    for i in range(num_filas):
        datos.append({
            "ID_Transaccion": f"TRX-{random.randint(10000, 99999)}",
            "Fecha": (fecha_base + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d"),
            "Cliente": random.choice(clientes),
            "Producto": random.choice(productos),
            "Cantidad": random.randint(1, 20),
            "Monto": round(random.uniform(150.0, 3500.0), 2)
        })
    return pd.DataFrame(datos)

def crear_archivo_masivo_limpio():
    # 5,000 filas de datos normales (lo que un sistema exportaría bien)
    df = generar_datos_base(5000)
    df.to_excel(os.path.join(CARPETA_ENTRADA, "01_historico_ventas_norte.xlsx"), index=False)

def crear_archivo_caotico_con_errores():
    # 2,000 filas, pero le inyectamos veneno del mundo real
    df = generar_datos_base(2000)
    
    # SOLUCIÓN: Convertimos las columnas a 'object' (genérico) para que Pandas 
    # nos permita inyectar texto donde originalmente había solo números.
    df['Monto'] = df['Monto'].astype(object)
    df['Cantidad'] = df['Cantidad'].astype(object)
    
    # Inyectar caos en "Monto" (Símbolos, textos raros, espacios)
    df.loc[10:50, 'Monto'] = df.loc[10:50, 'Monto'].apply(lambda x: f"$ {x:,.2f} MXN")
    df.loc[100:120, 'Monto'] = "Revisar precio"
    df.loc[500:505, 'Monto'] = "N/A"
    
    # Inyectar caos en "Cantidad"
    df.loc[300:310, 'Cantidad'] = "Sin stock"
    
    # Espacios fantasmas en los nombres de las columnas
    df.columns = [" ID_Transaccion ", "Fecha", " Cliente ", "Producto", "Cantidad", "  Monto  "]
    
    df.to_excel(os.path.join(CARPETA_ENTRADA, "02_reporte_sur_sucio.xlsx"), index=False)

def crear_archivo_con_duplicados_masivos():
    # 1,500 filas, pero vamos a clonar 500 filas exactamente iguales
    df = generar_datos_base(1000)
    df_clones = df.sample(500) # Tomamos 500 al azar y las duplicamos
    df_final = pd.concat([df, df_clones], ignore_index=True)
    
    # Desordenamos las filas para que los duplicados no estén juntos
    df_final = df_final.sample(frac=1).reset_index(drop=True)
    
    df_final.to_excel(os.path.join(CARPETA_ENTRADA, "03_exportacion_duplicada.xlsx"), index=False)

def crear_archivo_multihoyas_y_vacios():
    # Archivo de un usuario que usa Excel como libreta de notas
    df_datos = generar_datos_base(500)
    
    # Le falta la columna "Monto", para ver si nuestro pd.concat sobrevive a estructuras distintas
    df_incompleto = df_datos.drop(columns=["Monto"])
    
    ruta = os.path.join(CARPETA_ENTRADA, "04_reporte_mensual_varios.xlsx")
    with pd.ExcelWriter(ruta) as writer:
        df_datos.to_excel(writer, sheet_name="Enero", index=False)
        pd.DataFrame().to_excel(writer, sheet_name="Hoja Vacia 1", index=False)
        df_incompleto.to_excel(writer, sheet_name="Febrero (Incompleto)", index=False)
        
    # Archivo temporal que bloquea sistemas
    with open(os.path.join(CARPETA_ENTRADA, "~$archivo_fantasma.xlsx"), "w") as f:
        f.write("Basura")

def generar_todos():
    print("Creando carpeta y limpiando datos anteriores...")
    preparar_carpeta()
    
    print("Generando 01: 5,000 filas limpias...")
    crear_archivo_masivo_limpio()
    
    print("Generando 02: 2,000 filas con símbolos, textos inválidos y espacios trampa...")
    crear_archivo_caotico_con_errores()
    
    print("Generando 03: 1,500 filas con 500 duplicados exactos mezclados...")
    crear_archivo_con_duplicados_masivos()
    
    print("Generando 04: Múltiples hojas, hojas vacías y columnas faltantes...")
    crear_archivo_multihoyas_y_vacios()
    
    print("\n[LISTO] Se han generado más de 9,000 filas de datos de prueba realistas.")

if __name__ == "__main__":
    generar_todos()