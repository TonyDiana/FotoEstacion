#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Kernel del menú y la gestión de la exposición
    :Autor:     Tony Diana
    :Versión:   A15.1

    ---------------------------------------------------------------------------
"""
# -----------------------------------------------------------------------------
# Mapa de señales, mostrar Stacks, asociadas a señal 'realice'
# -----------------------------------------------------------------------------


# --- Módulos estandard
from std.gtk import Ventana
from std.disco import add_paths


# --- Deidades
from olimpo import ZEUS
from olimpo import HEISIS


# --- Módulos propios
from .. import const as KMENU


#
class GUI(Ventana):
    """ :Propósito: Clase manejadora del GUI de la exposición. """

    __slots__ = ["dif"]

    # --- Palabras mágicas
    __mg = {

        # --- Botones para activar y desactivar
        # --- Luz continua o flash
        "bt_fls_cont": ("_bt_flash_", "_bt_continua_"),

        # --- Puntual o evaluativa
        "bt_punt_eval": ("_bt_puntual_", "_bt_evaluativa_"),

        # --- Apertura o T/V
        "bt_ap_tv": ("_bt_apertura_", "_bt_tv_"),
        "zn_ap_tv": ("zn_apertura", "zn_tv"),
        "dts_ap_tv": ("dt_apertura", "dt_tv"),
        "dts_ap_tv_dec": ("dt_apertura_dec", "dt_tv_dec"),

        # --- Otras cosas a bloquear
        "bloquear": ("_bt_bloquear_", "_zona_ISO_", "zn_tv", "zn_apertura"),

        # --- Índice de la ayuda
        # HI_Exp

        # --- Archivos glade asociados
        # exp.glade, EXP
    }

    #
    def __init__(self):

        # --- Esta opción casi siempre responde que no hay respuesta
        # self.__resp = False

        # --- Marcadores globales de cargas diferidas de glade
        #   Ayuda
        self.dif = [True]

        # --- Crear ventana, 1º lista de glades
        path1 = add_paths(HEISIS.getPathTema, KMENU.SOMOS, "exp.glade")
        path2 = (ZEUS.getFileCSS, HEISIS.getFileCSS)

        Ventana.__init__(self, fileGlade=path1, fileCss=path2)
        del path1, path2

        #
        # --- Establecer valores iniciales

        # --- Módos de medición
        if HEISIS.esFlash:
            self.bt_flash()

        else:
            self.bt_continua()

        #
        if HEISIS.esPuntual:
            self.bt_puntual()

        else:
            self.bt_evaluativa()

        #
        if HEISIS.esApertura:
            self.bt_apertura()

        else:
            self.bt_tv()

        #
        # --- Tomar la ventana principal, conectar señales y mostrar
        self.ConectarSignals(self)
        self.win = self.GUI("EXP")
        self.win.show()

    #
    # --- Respuesta, siempre es nada
    #
    #
    @property
    def getRespuesta(self):
        return False

    #
    # --- Botones y señales
    #
    #
    # --- Sobreescritura del botón de salida, guardar datos
    def bt_exit(self, *args, **kwargs):
        HEISIS.Guardar()
        Ventana.bt_exit(self, *args, **kwargs)

    #
    # --- Solicitar ayuda
    def bt_help(self, *args, **kwargs):
        if self.dif[0]:   # --- Si nunca se hizo antes
            self.AgregarGlade(ZEUS.getFileGladeHelp)
            self.ConectarSignals(self)
            self.dif[0] = False

        self.MostrarUrl(ZEUS.urlHelp("HI_Exp"))

    #
    # --- Bloquear la exposición
    def bt_bloquear(self, *args, **kwargs):
        self.ActivoNO(self.__mg["bt_ap_tv"])
        self.ActivoNO(self.__mg["bloquear"])

    #
    # --- Modos de medición
    #
    #
    # --- Activar mediciones de flash
    def bt_flash(self, *args, **kwargs):
        self.ActivoSI(self.__mg["bt_fls_cont"][1])
        self.ActivoNO(self.__mg["bt_fls_cont"][0])
        HEISIS.esFlash = True

    #
    # --- Activar mediciones de luz continua
    def bt_continua(self, *args, **kwargs):
        self.ActivoSI(self.__mg["bt_fls_cont"][0])
        self.ActivoNO(self.__mg["bt_fls_cont"][1])
        HEISIS.esFlash = False

    #
    # --- Activar mediciones puntuales
    def bt_puntual(self, *args, **kwargs):
        self.ActivoSI(self.__mg["bt_punt_eval"][1])
        self.ActivoNO(self.__mg["bt_punt_eval"][0])
        HEISIS.esPuntual = True

    #
    # --- Activar mediciones de luz evaluativas
    def bt_evaluativa(self, *args, **kwargs):
        self.ActivoSI(self.__mg["bt_punt_eval"][0])
        self.ActivoNO(self.__mg["bt_punt_eval"][1])
        HEISIS.esPuntual = False

    #
    # --- Activar mediciones de aperturas
    def bt_apertura(self, *args, **kwargs):
        self.__unif__ap_tv(1, 0)
        HEISIS.esApertura = True

    #
    # --- Activar mediciones de T/V
    def bt_tv(self, *args, **kwargs):
        self.__unif__ap_tv(0, 1)
        HEISIS.esApertura = False

    #
    # --- Unificar ocultamiento y visualización de T/V y aperturas
    def __unif__ap_tv(self, uno, dos):
        self.ActivoSI(self.__mg["bt_ap_tv"][uno])
        self.Ocultar(self.__mg["zn_ap_tv"][uno])
        self.Mostrar(self.__mg["dts_ap_tv"][uno])
        self.Mostrar(self.__mg["dts_ap_tv_dec"][uno])

        self.ActivoNO(self.__mg["bt_ap_tv"][dos])
        self.Mostrar(self.__mg["zn_ap_tv"][dos])
        self.Ocultar(self.__mg["dts_ap_tv"][dos])
        self.Ocultar(self.__mg["dts_ap_tv_dec"][dos])
