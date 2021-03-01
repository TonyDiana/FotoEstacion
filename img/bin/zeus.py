#!/bin/python3
# -*- coding: utf-8 *-*
"""
    Entrada a la estación fotográfica
    :Autor:     Tony Diana
    :Versión:   A15.1
    ---------------------------------------------------------------------------
"""

# --- Módulos Deidades
from olimpo import ZEUS
from olimpo import HEISIS


# --- Módulos propios
from helioisis.main import HEISIS_main


# --- Sólo funcionar como módulo de arranque
if __name__ == "__main__":

    # --- Elevar a HelioIsis al nivel máximo e invocar a ZEUS
    ZEUS.Iniciar(HEISIS.getSoy)

    # --- Inicio de HelioIsis
    HEISIS_main()

    # --- Pedirle a ZEUS que finalice
    ZEUS.Acabar()

    # --- Y Shutdown
    if ZEUS.esShutdown:
        import os
        os.system('systemctl poweroff')
