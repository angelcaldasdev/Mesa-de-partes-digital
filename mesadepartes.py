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


# ----------------------------------------------------------------------
# ARREGLOS PARALELOS
# ----------------------------------------------------------------------
codigos = []
solicitantes = []
dnis = []
telefonos = []
barrios = []         # En lugar de distritos
direcciones = []
solicitudes = []
danos = []
atrapados = []
afectados = []
riesgos = []
puntajes = []
niveles = []

# ----------------------------------------------------------------------
# FUNCIONES DE CADENAS Y VALIDACIÓN
# ----------------------------------------------------------------------
def quitar_tildes(texto):
    origen = "áéíóúÁÉÍÓÚñÑ"
    destino = "aeiouAEIOUnN"
    resultado = ""
    for letra in texto:
        pos = origen.find(letra)
        if pos >= 0:
            resultado += destino[pos]
        else:
            resultado += letra
    return resultado

def buscar_barrio(texto):
    """Devuelve el nombre oficial del barrio de Santa Anita o '' si no se encuentra."""
    clave = quitar_tildes(texto.strip()).lower()
    for b in BARRIOS_SANTA_ANITA:
        if quitar_tildes(b).lower() == clave:
            return b
    return ""

def validar_dni(dni):
    return len(dni) == 8 and dni.isdigit()

def validar_telefono(tel):
    return len(tel) == 9 and tel.isdigit() and tel[0] == "9"

def validar_nombre(nombre):
    nombre = nombre.strip()
    if len(nombre) < 5:
        return False
    for letra in nombre:
        if not (letra.isalpha() or letra == " "):
            return False
    return True

def validar_texto(texto, minimo=5):
    texto = texto.strip()
    return len(texto) >= minimo and SEPARADOR not in texto

def validar_entero(texto, minimo, maximo):
    return texto.isdigit() and minimo <= int(texto) <= maximo

def validar_si_no(texto):
    return texto.strip().upper() in ("SI", "SÍ", "NO", "S", "N")

def normalizar(texto):
    return " ".join(p.capitalize() for p in texto.strip().split())