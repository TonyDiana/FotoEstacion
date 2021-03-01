#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Constantes de Helios
    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Necesitamos un trozo de las cámaras
from equipo.cam.const import ISOS as KISOS


# --- Identidad de Helios
from .version import VERSION
SOY = VERSION       # --- Evitar flake8 F401 de la constante VERSION
SOY = "helios"


# --- Fotometría --- Decoradores, sí soy muy terco con esto
DEC_UN_3 = " & 1/3"
DEC_DOS_3 = " & 2/3"


# - Razones fotométricas. Debido al alto uso de estas, siempre estarán en
#   memoria como costantes, aunque se carguen desde disco para permitir su
#   personalización.

# --- Este lo tomamos de las cámaras, en elementos
ISOS = KISOS


EFES = (
        "1", "1,1", "1,3", "1,4", "1,6", "1,8", "2", "2,2", "2,5", "2,8",
        "3,2", "3,6", "4", "4,5", "5", "5,6", "6,3", "7,1", "8", "9", "10",
        "11", "13", "14", "16", "18", "20", "22", "25", "29", "32", "36",
        "40", "45", "51", "57", "64", "72", "81", "91", "102", "114", "128"
    )

TIMES = (
        "1m", "50s", "40s", "30s", "25s", "20s", "15s", "13s", "10s", "8s",
        "6s", "5s", "4s", "3,2s", "2,5s", "2s", "1,6s", "1,3s", "1s", "0,8s",
        "0,6s", "0.5s", "0,4s", "0,3s", "4", "5", "6", "8", "10", "13", "15",
        "20", "25", "30", "40", "50", "60", "80", "100", "125", "160", "200",
        "250", "320", "400", "500", "640", "800", "1000", "1250", "1600",
        "2000", "2500", "3200", "4000", "5000", "6400", "8000"
    )
