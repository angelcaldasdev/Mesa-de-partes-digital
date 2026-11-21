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

        
# ----------------------------------------------------------------------
# BÚSQUEDA Y ORDENAMIENTO
# ----------------------------------------------------------------------
def buscar_lineal(codigo):
    codigo = codigo.strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == codigo:
            return i
    return -1

def indices_ordenados_por_codigo():
    orden = list(range(len(codigos)))
    for i in range(1, len(orden)):
        actual = orden[i]
        j = i - 1
        while j >= 0 and codigos[orden[j]] > codigos[actual]:
            orden[j + 1] = orden[j]
            j -= 1
        orden[j + 1] = actual
    return orden

def buscar_binaria(codigo):
    codigo = codigo.strip().upper()
    orden = indices_ordenados_por_codigo()
    izq, der = 0, len(orden) - 1
    while izq <= der:
        medio = (izq + der) // 2
        c = codigos[orden[medio]]
        if c == codigo:
            return orden[medio]
        elif c < codigo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1

def rango_nivel(nivel):
    return ["CRÍTICO", "ALTO", "MEDIO", "BAJO"].index(nivel)

def indices_priorizados():
    orden = list(range(len(codigos)))
    n = len(orden)
    for i in range(n - 1):
        mejor = i
        for j in range(i + 1, n):
            a, b = orden[j], orden[mejor]
            nivel_a, nivel_b = rango_nivel(niveles[a]), rango_nivel(niveles[b])
            if nivel_a < nivel_b:
                mejor = j
            elif nivel_a == nivel_b:
                if puntajes[a] > puntajes[b] or (puntajes[a] == puntajes[b] and codigos[a] < codigos[b]):
                    mejor = j
        orden[i], orden[mejor] = orden[mejor], orden[i]
    return orden


# ----------------------------------------------------------------------
# SALIDA POR PANTALLA
# ----------------------------------------------------------------------
def mostrar_detalle(i):
    print("  Código          :", codigos[i])
    print("  Solicitante     :", solicitantes[i], "(DNI " + dnis[i] + ", cel. " + telefonos[i] + ")")
    print("  Ubicación       :", direcciones[i] + " - " + barrios[i] + ", Santa Anita")
    print("  Tipo solicitud  :", solicitudes[i])
    print("  Tipo de daño    :", danos[i])
    print("  Heridos/atrapad.:", atrapados[i])
    print("  Personas afect. :", afectados[i])
    print("  Riesgo inminente:", riesgos[i])
    print("  Puntaje         :", puntajes[i], "-> Nivel", niveles[i])

def mostrar_tabla(orden, titulo):
    print()
    print("=" * 116)
    print(titulo)
    print("=" * 116)
    if len(orden) == 0:
        print("No hay expedientes registrados.")
        return
    formato = "{:<3} {:<14} {:<26} {:<24} {:<16} {:>4} {:>5} {:>6}  {:<8}"
    print(formato.format("N°", "CÓDIGO", "SOLICITANTE", "BARRIO/URB.", "TIPO DE DAÑO",
                         "ATR", "AFEC", "PUNTOS", "NIVEL"))
    print("-" * 116)
    pos = 1
    for i in orden:
        print(formato.format(pos, codigos[i], solicitantes[i][:26], barrios[i][:24],
                             DANO_CORTO[TIPOS_DANO.index(danos[i])], atrapados[i], afectados[i], puntajes[i], niveles[i]))
        pos += 1
    print("-" * 116)

def mostrar_todos_detalle():
    print()
    print("=" * 116)
    print("FICHAS COMPLETAS DE TODOS LOS EXPEDIENTES (SANTA ANITA)")
    print("=" * 116)
    if len(codigos) == 0:
        print("No hay expedientes registrados.")
        return
    for i in indices_ordenados_por_codigo():
        print("-" * 62)
        mostrar_detalle(i)
    print("-" * 62)
    print("Total impreso:", len(codigos), "expedientes")

def resumen_estadistico():
    print()
    print("RESUMEN ESTADÍSTICO - SANTA ANITA")
    print("-" * 44)
    print("Total de expedientes      :", len(codigos))
    print("Heridos / atrapados       :", sum(atrapados))
    print("Personas afectadas        :", sum(afectados))
    for nivel in ("CRÍTICO", "ALTO", "MEDIO", "BAJO"):
        cantidad = 0
        for n in niveles:
            if n == nivel:
                cantidad += 1
        print("Expedientes nivel {:<8}: {}".format(nivel, cantidad))

def exportar_reporte():
    nombre = "reporte_sismo_santa_anita.txt"
    with open(nombre, "w", encoding="utf-8") as f:
        f.write("MESA DE PARTES DIGITAL - SISMO (SANTA ANITA)\n")
        f.write("REPORTE DE EXPEDIENTES - LISTA PRIORIZADA\n")
        f.write("=" * 72 + "\n")
        pos = 1
        for i in indices_priorizados():
            f.write("\n{}. {}  |  {} pts  |  NIVEL {}\n".format(pos, codigos[i], puntajes[i], niveles[i]))
            f.write("   Solicitante : {} (DNI {}, cel. {})\n".format(solicitantes[i], dnis[i], telefonos[i]))
            f.write("   Ubicación   : {} - {}, Santa Anita\n".format(direcciones[i], barrios[i]))
            f.write("   Solicitud   : {}\n".format(solicitudes[i]))
            f.write("   Daño        : {}\n".format(danos[i]))
            f.write("   Heridos/atrapados: {} | Personas afectadas: {} | Riesgo inminente: {}\n".format(
                atrapados[i], afectados[i], riesgos[i]))
            pos += 1
        f.write("\n" + "=" * 72 + "\n")
        f.write("Total de expedientes: {}\n".format(len(codigos)))
    print("[OK] Reporte generado:", nombre)

    
# ----------------------------------------------------------------------
# ENTRADA DE DATOS CON VALIDACIÓN
# ----------------------------------------------------------------------
def pedir(mensaje, validador, error):
    while True:
        valor = input(mensaje).strip()
        if validador(valor):
            return valor
        print("  [!] " + error)

def pedir_opcion_lista(titulo, opciones):
    print(titulo)
    for k in range(len(opciones)):
        print("   {}. {}".format(k + 1, opciones[k]))
    while True:
        eleccion = input("  Elija una opción: ").strip()
        if validar_entero(eleccion, 1, len(opciones)):
            return opciones[int(eleccion) - 1]
        print("  [!] Opción fuera de rango.")

def registrar_interactivo():
    print("\n--- REGISTRO DE NUEVO EXPEDIENTE (SANTA ANITA) ---")
    nombre = pedir("Nombres y apellidos del solicitante: ", validar_nombre,
                   "Solo letras y espacios (mínimo 5 caracteres).")
    dni = pedir("DNI (8 dígitos): ", validar_dni, "El DNI debe tener 8 dígitos numéricos.")
    tel = pedir("Celular (9 dígitos, inicia con 9): ", validar_telefono, "Celular inválido.")
    barrio = pedir("Barrio o Urbanización de Santa Anita: ",
                    lambda t: buscar_barrio(t) != "",
                    "Barrio no válido. Escriba una zona válida (ej. Los Ficus, Nocheto, Universal).")
    direccion = pedir("Dirección o referencia específica: ", validar_texto,
                      "Ingrese una dirección de al menos 5 caracteres (sin el símbolo |).")
    solicitud = pedir_opcion_lista("Tipo de solicitud:", TIPOS_SOLICITUD)
    tipo_dano = pedir_opcion_lista("Tipo de daño:", TIPOS_DANO)
    n_atr = int(pedir("Personas heridas o atrapadas (0-500): ", lambda t: validar_entero(t, 0, 500),
                      "Ingrese un entero entre 0 y 500."))
    n_afe = int(pedir("Personas afectadas (0-5000): ", lambda t: validar_entero(t, 0, 5000),
                      "Ingrese un entero entre 0 y 5000."))
    riesgo = pedir("¿Hay riesgo inminente (gas, réplicas, colapso)? (SI/NO): ", validar_si_no,
                   "Responda SI o NO.")
    codigo = agregar_expediente(nombre, dni, tel, barrio, direccion, solicitud,
                                tipo_dano, n_atr, n_afe, riesgo)
    guardar_archivo()
    i = buscar_lineal(codigo)
    print("\n[OK] Expediente registrado y guardado. Código asignado:", codigo)
    print("     Clasificación automática:", niveles[i], "(" + str(puntajes[i]) + " puntos)")

def indices_codigos_texto():
    return [codigos[i] for i in indices_ordenados_por_codigo()]

def consultar_interactivo():
    codigo = input("Ingrese el código del expediente: ")
    i = buscar_binaria(codigo)
    if i == -1:
        print("[X] No se encontró el expediente", codigo.upper())
    else:
        print("\n[OK] Expediente encontrado:")
        mostrar_detalle(i)


# ----------------------------------------------------------------------
# DATOS DE PRUEBA DE SANTA ANITA
# ----------------------------------------------------------------------
DATOS_DEMO = [
    ("juan carlos quispe rojas", "45871236", "987654321", "Nocheto", "Jr. Los Robles 120",
     "Solicitud de ayuda", "Colapso de edificio o vivienda", 3, 40, "SI"),
    ("maría elena torres vega", "40123987", "912345678", "Los Ficus", "Av. Huancaray 450",
     "Pedido de atención", "Incendio o fuga de gas", 0, 25, "SI"),
    ("luis alberto mendoza paz", "70456123", "999111222", "Universal", "Calle 4 Mz. C",
     "Reporte de daños", "Vivienda con daños severos", 0, 12, "NO"),
    ("rosa angélica flores díaz", "32165498", "945612378", "El Asesor", "Calle Los Tulipanes",
     "Reporte de daños", "Vía bloqueada o puente dañado", 0, 30, "NO")
]

def cargar_ejemplos():
    limpiar_arreglos()
    for d in DATOS_DEMO:
        agregar_expediente(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9])
    guardar_archivo()
    print("Datos de ejemplo de Santa Anita cargados. Total:", len(codigos))
    