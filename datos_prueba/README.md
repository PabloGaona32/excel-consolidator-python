# Consolidador de Excel

Une varios archivos Excel con las mismas columnas en uno solo, sin perder ni duplicar filas, y genera un resumen y un reporte de problemas.

## Qué hace
- Lee todos los `.xlsx` de `datos_entrada/` (todas las hojas con datos).
- Alinea las columnas por nombre y quita espacios sobrantes en los encabezados.
- Agrega `archivo_origen` y `hoja_origen` a cada fila.
- Limpia montos escritos como texto (`$ 3,023.99 MXN`).
- Elimina filas duplicadas exactas y las guarda en una hoja aparte.
- Verifica que `filas leídas = filas finales + duplicados eliminados`. Si no cuadra, no genera el archivo.

## Instalación
```bash
pip install -r requirements.txt
```
Requiere Python 3.10 o superior.

## Uso
1. Copia tus archivos `.xlsx` en `datos_entrada/`.
2. Ajusta `config.py` si hace falta (`QUITAR_DUPLICADOS`, `COLUMNAS_A_SUMAR` y las columnas obligatorias).
3. Ejecuta:
```bash
python main.py
```
4. Revisa `salida/consolidado.xlsx` y el log en `logs/`.

## Qué trae el archivo de salida
| Hoja | Contenido |
|---|---|
| Maestra | Todas las filas unidas |
| Duplicados_Eliminados | Filas repetidas que se quitaron |
| Revision | Hojas vacías, columnas faltantes, texto inválido |
| Resumen | Totales de filas, filas por archivo y sumas |

## Reglas y decisiones
- Si una celda numérica tiene texto que no se puede convertir (ej. "Sin stock"), se deja vacía y se reporta en `Revision`.
- Si a una hoja le faltan columnas obligatorias, se avisa en `Revision` pero se incluye.
- Los archivos temporales (`~$`) y los que no son `.xlsx` se ignoran y se anotan en el log.

## Pruebas
```bash
python -m unittest discover tests
```