import os

# ==========================================
# CONFIGURACIÓN GENERAL DEL PROYECTO
# ==========================================

# Rutas de las carpetas principales. 
# Usamos variables aquí para no tener que buscar estas rutas por todo el código si decidimos cambiarlas.
CARPETA_ENTRADA = "datos_entrada"
CARPETA_SALIDA = "salida"
CARPETA_LOGS = "logs"

# Nombre del archivo final que vamos a generar
ARCHIVO_SALIDA = os.path.join(CARPETA_SALIDA, "consolidado.xlsx")

# ==========================================
# REGLAS DE NEGOCIO
# ==========================================

# Si es True, eliminará las filas que sean exactamente iguales en todas sus columnas.
# Si es False, las dejará intactas en la hoja Maestra.
QUITAR_DUPLICADOS = True

# Lista de columnas numéricas que queremos sumar en la hoja de 'Resumen'.
# Aquí pondremos nombres de ejemplo que luego nuestro generador de pruebas usará.
COLUMNAS_A_SUMAR = ["Monto", "Cantidad"]

COLUMNAS_OBLIGATORIAS = ["ID_Transaccion", "Fecha", "Cliente", "Producto", "Cantidad", "Monto"]