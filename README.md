# Mesa de Partes Digital - Sismo (Santa Anita)

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/angelcaldasdev/Mesa-de-partes-digital/blob/main/Mesa_de_partes_colab.ipynb)

Prototipo en Python para registrar reportes de daños, solicitudes de ayuda y
pedidos de atención después de un sismo de gran magnitud, enfocado en el
distrito de Santa Anita (Lima).

**Curso:** Fundamentos de Programación (CIIN1205P) - UPN

## Funcionalidades
- Registro de expedientes con validación de datos (DNI, celular, barrio, etc.)
- Clasificación automática por nivel de riesgo: Crítico, Alto, Medio y Bajo
- Búsqueda lineal y binaria por código de expediente
- Ordenamiento por código y lista priorizada por gravedad
- Persistencia de datos en archivo de texto
- Resumen estadístico y reporte exportable para imprimir

## Probarlo en línea (sin instalar nada)
Haz clic en el botón **Abrir en Google Colab** de arriba y ejecuta las celdas
en orden. El menú aparecerá en la última celda.

## Descargar y ejecutar en tu computadora

### Requisitos
- Python 3.8 o superior ([descargar Python](https://www.python.org/downloads/))
- No necesita librerías externas

### Opción 1: con Git
```bash
git clone https://github.com/angelcaldasdev/Mesa-de-partes-digital.git
cd Mesa-de-partes-digital
python mesadepartes.py
```

### Opción 2: sin Git
1. Haz clic en el botón verde **Code** de este repositorio.
2. Elige **Download ZIP** y descomprímelo.
3. Abre la carpeta en una terminal y ejecuta:
```bash
python mesadepartes.py
```

> En Mac o Linux usa `python3 mesadepartes.py`. En Windows, si `python` no
> funciona, prueba con `py mesadepartes.py`.

## Menú principal
| Opción | Acción |
|--------|--------|
| 1 | Registrar expediente |
| 2 | Consultar expediente por código |
| 3 | Listar expedientes ordenados por código |
| 4 | Lista priorizada (Crítico, Alto, Medio, Bajo) |
| 5 | Resumen estadístico |
| 6 | Cargar expedientes de ejemplo |
| 7 | Exportar reporte para imprimir |
| 0 | Salir |

## Autor
Angel Caldas Ocmin - [@angelcaldasdev](https://github.com/angelcaldasdev)
Elber Nuñez Iguavel
Milovan Rojas Romero