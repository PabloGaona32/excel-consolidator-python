# Consolidador de Excel

Une varios archivos de Excel con las mismas columnas en un solo archivo, sin perder ni duplicar filas por error. Además genera un resumen, un reporte de problemas y un log de cada ejecución.

Pensado para casos reales: archivos de distintas sucursales o meses, con encabezados desordenados, montos escritos como texto, hojas vacías y filas repetidas.

## Qué hace

- Lee todos los archivos `.xlsx` de la carpeta `datos_entrada/` y todas las hojas que tengan datos.
- Alinea las columnas por nombre (no por posición) y quita espacios sobrantes en los encabezados.
- Agrega dos columnas a cada fila para saber de dónde viene: `archivo_origen` y `hoja_origen`.
- Limpia montos y cantidades escritos como texto (por ejemplo `$ 3,023.99 MXN` pasa a `3023.99`).
- Elimina las filas duplicadas exactas y las guarda en una hoja aparte para poder revisarlas.
- Avisa cuando a una hoja le faltan columnas obligatorias.
- Verifica que `filas leídas = filas finales + duplicados eliminados`. Si las cuentas no cuadran, **no genera el archivo** y lo deja anotado en el log.
- Si un archivo está dañado o no se puede abrir, lo anota y sigue con los demás.

## Requisitos

- Python 3.10 o superior
- Librerías: `pandas` y `openpyxl`

```bash
pip install -r requirements.txt
```

## Cómo usarlo

1. Copia tus archivos `.xlsx` en la carpeta `datos_entrada/`.
2. Si hace falta, ajusta las reglas en `config.py` (ver más abajo).
3. Ejecuta:

```bash
python main.py
```

4. Abre `salida/consolidado.xlsx` y revisa el log en `logs/`.

> Cierra el archivo `consolidado.xlsx` antes de volver a ejecutar. Si está abierto en Excel, el programa no puede reemplazarlo y se detiene con un aviso.

## Configuración (`config.py`)

| Opción | Para qué sirve |
|---|---|
| `QUITAR_DUPLICADOS` | `True` elimina filas idénticas en todas sus columnas. `False` las deja en la hoja Maestra. |
| `COLUMNAS_A_SUMAR` | Columnas numéricas que se suman en el Resumen (por defecto `Monto` y `Cantidad`). |
| `COLUMNAS_OBLIGATORIAS` | Columnas que debe tener cada hoja. Si falta alguna, se avisa en `Revision`. |
| `CARPETA_ENTRADA`, `CARPETA_SALIDA`, `CARPETA_LOGS` | Rutas de las carpetas. |

Para usar el programa con otras columnas, cambia `COLUMNAS_A_SUMAR` y `COLUMNAS_OBLIGATORIAS`.

## Qué trae el archivo de salida

| Hoja | Contenido |
|---|---|
| `Maestra` | Todas las filas unidas, con `archivo_origen` y `hoja_origen`. |
| `Duplicados_Eliminados` | Las filas repetidas que se quitaron. |
| `Revision` | Hojas vacías, columnas que faltan y celdas con texto donde debía haber un número. |
| `Resumen` | Total de filas leídas, duplicadas y finales, filas aportadas por cada archivo y sumas de las columnas numéricas. |

## Log de cada ejecución

En `logs/` se guarda un archivo por corrida (`ejecucion_FECHA.txt`) con:

- Estado: `ÉXITO` o `ERROR CRÍTICO`.
- Dónde quedó el archivo generado.
- Archivos procesados y archivos ignorados (temporales `~$` u otros formatos).
- Contabilidad de filas y sumas de las columnas numéricas.
- Detalle de todas las alertas.

## Ejemplo de resultado

Con 4 archivos de prueba:

```
Filas leídas originales : 9500
Filas finales en maestra: 9000
Duplicados eliminados   : 500
Monto:    15,358,033.71
Cantidad: 93,663.00
```

Alertas que reportó:

- Una hoja vacía, que se ignoró.
- 21 celdas de `Monto` con texto no numérico ("Revisar precio"), que se dejaron vacías.
- 11 celdas de `Cantidad` con texto ("Sin stock"), que se dejaron vacías.
- Una hoja sin la columna obligatoria `Monto`.

## Estructura del proyecto

```
├── main.py              # Punto de entrada
├── config.py            # Reglas y rutas
├── requirements.txt
├── src/
│   ├── leer_archivos.py # Busca y lee los Excel
│   ├── validar.py       # Alinea columnas y limpia números
│   ├── consolidar.py    # Une las hojas y quita duplicados
│   ├── resumen.py       # Calcula totales y sumas
│   └── exportar.py      # Escribe el Excel final
├── datos_entrada/       # Aquí van los archivos a consolidar
├── datos_prueba/        # Archivos de ejemplo (datos inventados)
├── salida/              # Aquí queda consolidado.xlsx
└── logs/                # Un log por ejecución
```

## Reglas y decisiones

- Un duplicado es una fila idéntica en todas sus columnas de datos. Se conserva la primera aparición.
- Si una celda de una columna numérica tiene texto que no se puede convertir, se deja vacía y se reporta en `Revision`. La fila **no se elimina**.
- Si a una hoja le faltan columnas obligatorias, se avisa en `Revision`, pero sus filas se incluyen en la hoja Maestra.
- Los archivos temporales de Excel (`~$`) y los que no son `.xlsx` se ignoran y se anotan en el log.

## Límites conocidos

- Solo lee archivos `.xlsx` (no `.xls` ni `.csv`).
- Espera los encabezados en la primera fila de cada hoja. No detecta títulos arriba de la tabla ni filas de totales al final.
- Pensado para números con punto decimal (`1200.50`). No interpreta formatos como `1.200,50`.
- Distingue mayúsculas y minúsculas en los nombres de columna.

Cada cliente tiene archivos distintos, así que casi siempre hace falta adaptar el programa a su caso (columnas, reglas de duplicados, formatos). Eso se resuelve cambiando `config.py` o ajustando el código de `src/`.

## Contacto

pablogaonarz32@gmail.com