#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Menú principal de HelioIsis.
    :Autor:     Tony Diana
    :Versión:   A8.1

    ---------------------------------------------------------------------------
"""

# --- Módulos estandard
from std.gtk import Ventana
from std.disco import add_paths


# --- Deidades
from olimpo import ZEUS
from olimpo import HEISIS


# --- Equipo
from equipo import GUICam


# --- Módulos propios
from . import const as KMENU
from . import setup, calculos
from . exp import kernel as EXPOSION
from .ismtp import MailMain


#
def GO() -> None:
    """ :Propósito: Bucle del menú de HelioIsis. """

    # --- Función genérica para el manejo de un menú estandarizado
    def menu_std(Objeto: object):
        Objeto.Main()
        x = Objeto.getRespuesta
        del Objeto
        return x

    #
    # --- Montaje del menú: funciones y opciones
    switcher = {
        KMENU.Option.SALIR: lambda: None,

        KMENU.Option.MAIN: lambda: menu_std(GUI()),
        KMENU.Option.SETUP: lambda: menu_std(setup.GUI()),
        KMENU.Option.EXP: lambda: menu_std(EXPOSION.GUI()),
        KMENU.Option.CALC: lambda: menu_std(calculos.GUI()),


        KMENU.Option.CAM: lambda: menu_std(GUICam())

    }
    option = KMENU.Option.MAIN

    #
    # --- Bucle del menú
    while True:

        ZEUS.RecolectarBasura()
        try:
            # --- Primero busquemos un i-mail con instrucciones
            mail = MailMain()
            if (mail.RecibirMailYBorrar()):
                option = mail.adonde

            del mail

            # --- Ejecutamos función asociada a la opción
            resp = switcher[option]()

            # --- Analizando la respuesta
            if resp:
                # --- Salida
                if resp == KMENU.Option.SALIR:
                    break

                # --- Instrucciones especiales
                else:
                    # --- Solicitud de una opción específica del menú
                    if resp in switcher:
                        option = resp

            # --- Sin respuesta, volver al menú principal
            else:
                option = KMENU.Option.MAIN

        except Exception:
            # --- Ante cualquier problema, volver al menú principal
            option = KMENU.Option.MAIN

    #
    # --- Cuando todo acaba HelioIsis debe ejecutar su fin
    HEISIS.Fin()


#
class GUI(Ventana):
    """ :Propósito: Clase manejadora del GUI del menú principal. """

    __slots__ = ["__resp", "help"]

    # --- Palabras mágicas
    __mg = {
        # --- Índice de la ayuda
        "help": "HI_HOME",

        # --- GtkWindow
        "w_dev": "devolver",
        "w_qr": "qr",
        # main

        # --- Datos varios
        # MAIN_VERSION, MAIN_USU_NAME, DEVOLVER_USU_NAME, MAIN_USU_MAIL,
        # DEVOLVER_USU_MAIL, MSG_DEV

        # --- Archivo glade asociado
        # "main.glade"
    }

    #
    def __init__(self):
        # --- Respuesta
        self.__resp: int = False

        # --- Marcadores globales de cargas diferidas de glade
        self.help = True

        # --- Crear ventana
        path1 = add_paths(HEISIS.getPathTema, KMENU.SOMOS, "main.glade")
        path2 = (ZEUS.getFileCSS, HEISIS.getFileCSS)

        Ventana.__init__(self, fileGlade=path1, fileCss=path2)
        del path1, path2

        # --- Rellenar datos
        self.SetTexto("MAIN_VERSION", HEISIS.getVersion)
        self.SetTexto("MAIN_USU_NAME", ZEUS.nombreUsuario)
        self.SetTexto("DEVOLVER_USU_NAME", ZEUS.nombreUsuario)
        self.SetTexto("MAIN_USU_MAIL", ZEUS.mailUsuario)
        self.SetTexto("DEVOLVER_USU_MAIL", ZEUS.mailUsuario)
        self.SetTexto("MSG_DEV", HEISIS.msg)

        # --- Tomar la ventana principal, conectar señales y mostrar
        self.ConectarSignals(self)
        self.win = self.GUI("main")
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
    # --- Salir de la App
    def bt_exit(self, *args, **kwargs):
        self.__resp = KMENU.Option.SALIR
        Ventana.bt_exit(self, *args, **kwargs)

    # --- Solicitar ayuda
    def bt_help(self, *args, **kwargs):
        # --- Si nunca se hizo antes
        if self.help:
            self.AgregarGlade(ZEUS.getFileGladeHelp)
            self.ConectarSignals(self)
            self.help = False

        self.MostrarUrl(ZEUS.urlHelp(self.__mg["help"]))

    #
    # --- Ir a la exposición
    def bt_exp(self, *args, **kwargs):
        self.__resp = KMENU.Option.EXP
        Ventana.bt_exit(self, *args, **kwargs)

    #
    # --- Ir al setup
    def bt_setup(self, *args, **kwargs):
        self.__resp = KMENU.Option.SETUP
        Ventana.bt_exit(self, *args, **kwargs)

    #
    # --- Ir a cálculos
    def bt_regla(self, *args, **kwargs):
        self.__resp = KMENU.Option.CALC
        Ventana.bt_exit(self, *args, **kwargs)

    #
    # --- Entrar la pantalla que solicita devolver al propietario
    def bt_devolver_on(self, *args, **kwargs):
        self.Mostrar(self.__mg["w_dev"])

    #
    # --- Salir de la pantalla que solicita devolver al propietario
    def bt_devolver_off(self, *args, **kwargs):
        self.Ocultar(self.__mg["w_dev"])

    #
    # --- Mostrar el código QR
    def bt_cartel_on(self, *args, **kwargs):
        self.Mostrar(self.__mg["w_qr"])

    #
    # --- Ocultar el código QR
    def bt_cartel_off(self, *args, **kwargs):
        self.Ocultar(self.__mg["w_qr"])

    #
    # --- Salir de la app
    def bt_qr(self, *args, **kwargs):
        import sys
        sys.exit()
