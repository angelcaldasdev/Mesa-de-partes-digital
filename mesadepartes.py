# -*- coding: utf-8 -*-
"""
Mesa de Partes Digital - Sismo (Santa Anita, Lima)
Curso: Fundamentos de Programación (CIIN1205P) - UPN

Prototipo para registrar reportes de daños, solicitudes de ayuda y pedidos de
atención después de un terremoto de gran magnitud, enfocado en el distrito de
SANTA ANITA y sus barrios/urbanizaciones.
"""

import os
import sys

# Evita errores de codificación (tildes) en la consola de Windows
for _flujo in (sys.stdout, sys.stdin):
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ----------------------------------------------------------------------
# CONSTANTES
# ----------------------------------------------------------------------
ARCHIVO = "expedientes_sismo_santa_anita.txt"
SEPARADOR = "|"
ANIO = 2026

TIPOS_SOLICITUD = ["Reporte de daños", "Solicitud de ayuda", "Pedido de atención"]

# Tipo de daño y puntaje base
TIPOS_DANO = ["Colapso de edificio o vivienda", "Incendio o fuga de gas",
              "Vivienda con daños severos", "Vía bloqueada o puente dañado",
              "Corte de agua o luz", "Grietas leves"]
PUNTOS_DANO = [60, 50, 40, 20, 20, 10]
DANO_CORTO = ["Colapso", "Incendio/gas", "Daño severo", "Vía bloqueada", "Corte servicios", "Grietas leves"]

# Urbanizaciones, cooperativas y barrios conocidos de Santa Anita
BARRIOS_SANTA_ANITA = [
    "Los Ficus", "Universal", "Nocheto", "El Asesor", "Sausalito",
    "Covima", "La Santa Anita", "San Francisco", "Virgen de las Mercedes",
    "Los Productores", "Villas de Santa Anita", "Los Perales", "Chancas de Andahuaylas"
]