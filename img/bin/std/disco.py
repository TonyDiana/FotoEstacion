#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores globales de acceso al disco
    :Autor:     Tony Diana
    :Versión:   21.01.15

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import os
import shutil

from pathlib import Path    # --- Manejador de path's, Pathlib


#
def add_paths(*args) -> str:
    """
    :Propósito: Sumar paths y dejarlos correctos, según el **SO** utilizado.

    :param args: Path's a sumar.
    :type args: string

    :return: Cadena path normalizada con los siguientes efectos:

        1) Sumado de path's según el sistema operativo.
        2) Sustituir **~** por [HOME].
    """

    # --- Hace falta sumar el path de ejecución
    # path = os.path.join(os.chdir(os.path.dirname(__file__)), path)
    path = os.path.join(*args)

    # --- Normalización de linux
    try:
        path = path.replace('~', os.environ['HOME'])

    except Exception:
        path = path

    return path


#
def mi_path() -> str:
    """
    :Propósito: Obtener el path actual de ejecución.
    :return: Path actual de ejecución (string).
    """
    return os.getcwd()


#
def recorrer_path(path: str) -> list:
    """
    :Propósito: Recorrer un path y ofrecer una lista con el contenido.

    :param path: Path a recorrer.
    :type path: string

    :return: (lista) -  Contenido del path.

    .. nota::
        Sólo ofrece paths, no ofrece lista de archivos
    """

    lista = list()
    for x in Path(path).iterdir():
        if x.is_dir():          # --- Sólo directorios
            y = x.parts[-1]     # --- Sujeto dentro del path
            if y[:2] != '__':   # --- No objetos Python (is_dir devuelve True)
                lista.append(y)

    return lista


#
def mkdir(path: str) -> None:
    """
        Crear un directorio si no existe. Si se le pasa como argumento un
        nombre de archivo, extrae el nombre de la carpeta para crear el path.
    """
    path = os.path.dirname(path)
    if not(os.path.exists(path)):
        os.mkdir(path)


#
def copydir(origen: str, destino: str) -> bool:
    """
        Copia el árbol de directorios de origen a destino, borrando primero
        el árbol destino. Controla el error si la carpeta **destino** no existe
        y devuelve ``True`` si lo logra. Si no lo logra devuelve ``False``.
    """
    shutil.rmtree(destino, ignore_errors=True)

    try:
        shutil.copytree(origen, destino, symlinks=False, ignore=None,
                        ignore_dangling_symlinks=False)
        return True

    except Exception:
        return False
