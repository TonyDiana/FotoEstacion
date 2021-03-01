#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Simplificar la invocación de equipo:

        **Cámaras**

        - ``from equipo import MailGUICam``: Mail al GUI de cámaras.
        - ``from equipo import GUICam``: GUI de cámaras.
        - ``from equipo import ClassCam``: Objeto manejador de una cámara.
        - ``from equipo import ListaCam``: Objeto manejador lista de cámaras.

    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Cámaras
from .cam.GUI import MailGUICam
from .cam.GUI import GUI as GUICam
from .cam.kernel import ClassCAM, ListaCAM


# --- Evitar error de flake8 F401
a = MailGUICam
a = GUICam
a = ListaCAM
a = ClassCAM
del a
