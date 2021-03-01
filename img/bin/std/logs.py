#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores globales de archivos de log
    :Autor:     Tony Diana
    :Versión:   21.01.24

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python, Registro de log's
import logging


# --- Módulos estandard
from .disco import mkdir


# --- Constantes propias, objetos manejadores del error
global OBJ_ERROR, OBJ_INFO, ESLOGACTIVO
ESLOGACTIVO = False


#
def log_ERROR(programa: str, ente: str, mensaje: str) -> None:
    """
    :Propósito: Producir un registro de log de ERROR.
    :returns:   Nada

    :param programa: Programa que invoca el log.
    :param ente: Nombre del ente. Se recomienda suministrar
                        ``__name__`` + "." + ``self.__class__.__name__``.
    :param mensaje:     Mensaje adicional.
    """

    # --- Sólo si están activos los logs
    global OBJ_ERROR
    if ESLOGACTIVO:
        OBJ_ERROR.error(__log_msg(programa, ente, mensaje))


#
def log_INFO(programa: str, ente: str, mensaje: str) -> None:
    """
    :Propósito: Producir un registro de log de INFO.

    :param programa: Programa que invoca el log.
    :param ente: Nombre del ente. Se recomienda suministrar
                        ``__name__`` + "." + ``self.__class__.__name__``.
    :param mensaje:     Mensaje adicional.
    """
    # --- Sólo si están activos los logs
    global OBJ_INFO
    if ESLOGACTIVO:
        OBJ_INFO.info(__log_msg(programa, ente, mensaje))


#
def iniciar_logs(fileErrores: str, fileInfo: str) -> None:
    """
    :Propósito: Inicial el registro de logs.
    :returns: Nada

    :fileErrores: Archivo .csv donde se almacenarán los mensajes de error.
    :fileinfo: Archivo .csv donde se almacenarán los mensajes de información.

    :Formato del registro log:
        :Fecha: AAAA-MM-DD HH:MM:SS,mmm (mmm = Milésima de segundo)
        :nivel: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET.
        :mensaje: Mensaje enviado al log

    .. warning::
        Sólo se han activado los niveles de ``Error`` e ``Info``. Además, y
        puesto que el log debe arrancar después de leer la configuración, si no
        se logra crear la carpeta de la base de datos, se puede producir una
        excepción.
    """

    # --- Activar los log's
    global OBJ_ERROR, OBJ_INFO
    OBJ_ERROR = _activar_log(logging.ERROR, fileErrores)
    OBJ_INFO = _activar_log(logging.INFO, fileInfo)
    log_Activar()


#
def log_to_list(file: str) -> list:
    """
    :Propósito:
        Convierte el archivo **.csv** de log a una lista Python utilizable
        en una ListStore.
    :returns: Lista con el archivo de log.

    :file: Path + Archivo ``.csv`` donde están almacenados los mensajes de log.

    .. Nota::
        Ofrece la lista ordenada del mensaje más nuevo al más viejo.
    """

    # --- Librería estándard Python
    import csv

    # --- 1º montar en una lista
    lista = []
    with open(file, 'r') as archivo:
        manejador = csv.reader(archivo)

        for reg in manejador:
            lista.append(reg)

    lista.reverse()

    # --- 2º preparar como se necesita
    ret = []
    for x in lista:
        try:
            temp = (x[0], x[4])
            ret.append(temp)

        except Exception:
            # --- Si fué manipulado el archivo, no producirá error
            temp = False

    return ret


#
def log_Activar() -> None:
    """ Activar la acción de los logger. """
    global ESLOGACTIVO
    ESLOGACTIVO = True


#
def log_Desactivar() -> None:
    """ Activar la acción de los logger. """
    global ESLOGACTIVO
    ESLOGACTIVO = False


# --- Activar el log de Error, código estandard Python, póco que inventar
def _activar_log(nivel: str, archivo: str):

    # --- 1º crear la carpeta
    mkdir(archivo)

    logeador = logging.getLogger()
    logeador.setLevel(nivel)

    manejador = logging.FileHandler(archivo)
    manejador.setLevel(nivel)

    # --- Formato del registro, nivel estandard de la librería
    formato = logging.Formatter(
        '"%(asctime)s","%(levelname)-s","%(message)s"'
    )
    manejador.setFormatter(formato)
    logeador.addHandler(manejador)
    return logeador


# --- Unificación de los mensajes de log
def __log_msg(programa: str, ente: str, mensaje: str) -> str:
    return '%s","%s","%s' % (programa, ente, mensaje)
