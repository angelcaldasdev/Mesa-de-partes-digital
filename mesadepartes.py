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


# ----------------------------------------------------------------------
# LÓGICA DE NEGOCIO: CLASIFICACIÓN AUTOMÁTICA
# ----------------------------------------------------------------------
def calcular_puntaje(tipo_dano, n_atrapados, n_afectados, riesgo):
    base = PUNTOS_DANO[TIPOS_DANO.index(tipo_dano)]
    extra_riesgo = 40 if riesgo == "SI" else 0
    return base + n_atrapados * 25 + n_afectados * 2 + extra_riesgo

def clasificar_nivel(puntaje, n_atrapados):
    if n_atrapados >= 1:
        return "CRÍTICO"
    if puntaje >= 150:
        return "CRÍTICO"
    elif puntaje >= 80:
        return "ALTO"
    elif puntaje >= 30:
        return "MEDIO"
    return "BAJO"

def generar_codigo():
    mayor = 0
    for c in codigos:
        numero = int(c.split("-")[2])
        if numero > mayor:
            mayor = numero
    return "SIS-" + str(ANIO) + "-" + str(mayor + 1).zfill(4)

def agregar_expediente(nombre, dni, tel, barrio, direccion, solicitud,
                       tipo_dano, n_atr, n_afe, riesgo):
    codigo = generar_codigo()
    riesgo = "SI" if riesgo.strip().upper() in ("SI", "SÍ", "S") else "NO"
    puntaje = calcular_puntaje(tipo_dano, n_atr, n_afe, riesgo)
    codigos.append(codigo)
    solicitantes.append(normalizar(nombre))
    dnis.append(dni)
    telefonos.append(tel)
    barrios.append(buscar_barrio(barrio))
    direcciones.append(direccion.strip())
    solicitudes.append(solicitud)
    danos.append(tipo_dano)
    atrapados.append(n_atr)
    afectados.append(n_afe)
    riesgos.append(riesgo)
    puntajes.append(puntaje)
    niveles.append(clasificar_nivel(puntaje, n_atr))
    return codigo


# ----------------------------------------------------------------------
# PERSISTENCIA EN ARCHIVOS
# ----------------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for i in range(len(codigos)):
            linea = SEPARADOR.join([
                codigos[i], solicitantes[i], dnis[i], telefonos[i],
                barrios[i], direcciones[i], solicitudes[i], danos[i],
                str(atrapados[i]), str(afectados[i]), riesgos[i]
            ])
            f.write(linea + "\n")

def cargar_archivo():
    limpiar_arreglos()
    if not os.path.exists(ARCHIVO):
        return 0
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        for linea in f:
            p = linea.strip().split(SEPARADOR)
            if len(p) != 11:
                continue
            if p[7] not in TIPOS_DANO:
                continue
            puntaje = calcular_puntaje(p[7], int(p[8]), int(p[9]), p[10])
            codigos.append(p[0])
            solicitantes.append(p[1])
            dnis.append(p[2])
            telefonos.append(p[3])
            barrios.append(p[4])
            direcciones.append(p[5])
            solicitudes.append(p[6])
            danos.append(p[7])
            atrapados.append(int(p[8]))
            afectados.append(int(p[9]))
            riesgos.append(p[10])
            puntajes.append(puntaje)
            niveles.append(clasificar_nivel(puntaje, int(p[8])))
    return len(codigos)

def limpiar_arreglos():
    for arreglo in (codigos, solicitantes, dnis, telefonos, barrios, direcciones,
                    solicitudes, danos, atrapados, afectados, riesgos, puntajes, niveles):
        arreglo.clear()