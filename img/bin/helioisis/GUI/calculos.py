#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Menú de los cálculos de cámara (Hiperfocal, etc...)
    :Autor:     Tony Diana
    :Versión:   A7.2

    ---------------------------------------------------------------------------
"""
# -----------------------------------------------------------------------------
# Mapa de señales, mostrar Stacks, asociadas a señal 'realice'
# sg_gen_usu_realice    sg_par_nube_realice     sg_cam_lent_realice
# sg_par_deco_realice   sg_gen_cam_realice
# -----------------------------------------------------------------------------


# --- Módulos estandard
from std.gtk import Ventana
from std.disco import add_paths


# --- Deidades
from olimpo import ZEUS
from olimpo import HELIOS
from olimpo import HEISIS


# --- Módulos propios
from . import const as KMENU
from .ismtp import MailMain, MailSetup


#
class GUI(Ventana):
    """ :Propósito: Clase manejadora del GUI del menú del setup. """

    __slots__ = ["__resp", "win", "help", "sele", "conf"]

    # --- Palabras mágicas
    __mg = {

        # --- Lugares a regresar
        "rg_cam": "REG_CAM",    # --- Regresar a las cámaras
        "rg_lent": "REG_LENT",  # --- Regresar a las lentes

        # --- Índice de la ayuda
        # HI_Setup

        # --- GtkWindow principal
        # SETUP

        # --- Botones

        # --- GtkEntry's

        # --- GtkStacks's

        # --- Gestores de listas

        # --- Archivos glade asociados
        # setup.glade
    }

    #
    def __init__(self):

        # --- Este menú casi siempre responde que no hay respuesta
        self.__resp = False

        # --- Marcadores globales de cargas diferidas de glade
        self.help = True
        self.sele = True
        self.conf = True

        # --- Crear ventana, 1º lista de glades
        path1 = add_paths(HEISIS.getPathTema, KMENU.SOMOS, "setup.glade")
        path2 = (ZEUS.getFileCSS, HEISIS.getFileCSS)

        Ventana.__init__(self, fileGlade=path1, fileCss=path2)
        del path1, path2

        # --- Tomar la ventana principal, conectar señales y mostrar
        self.ConectarSignals(self)
        self.win = self.GUI("SETUP")
        self.win.show()

    #
    # --- Respuestas
    #
    #
    @property
    def getRespuesta(self):
        return self.__resp

    #
    # --- Botones y señales
    #
    #
    # --- Destruir ventana. Botón salir.
    def bt_exit(self, *args, **kwargs):
        self.win.destroy()
        self.Quit(self, *args, **kwargs)

    #
    # --- Métodos privados
    #
    #
    # --- Activar una página del Stack
    def __stack(self, stack, pagina):
        tmp = self.GUI(stack)
        tmp.set_visible_child_name(pagina)
