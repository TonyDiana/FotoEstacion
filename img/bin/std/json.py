#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores globales de cadenas json.
    :Autor:     Tony Diana
    :Versión:   21.01.22

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import json


# --- Módulos estandard
from .datos import auto, EnteDatos, leer_archivo_texto, guardar_archivo_texto


# --- Extensión de los archivos
EXT = ".json"


#
def leer_archivo_json(programa: str, nfile: str, dic_data: dict,
                      eliminaFecha: bool = True) -> bool:
    """
    :Propósito: Leer un archivo json del disco.

    :param programa: Nombre del programa para log de errores.
    :type programa: string

    :param nfile: Nombre de archivo con path completo y sin extensión.
    :type nfile: string

    :param dic_data: Diccionario que recibirá los datos (se trata como puntero)
    :type dic_data: string

    :param eliminaFecha:
        En caso de recibir un ``True``, elimina de la cabecera la fecha de
        generación antes de devolver el json
    :type eliminaFecha: bool

    :returns:
        Devuelve un ``True`` si logra leerlo, y un ``False`` sin no lo logra.
    """
    file = nfile + EXT
    funct = json.load   # --- Función efectiva
    return leer_archivo_texto(funct, programa, file, dic_data, eliminaFecha)


#
def guardar_archivo_json(programa: str, nfile: str, dic_data: dict,
                         agregaFecha: bool = True) -> bool:
    """
    :Propósito: Guardar un archivo json en disco. Si hay error produce mensaje
                 en el registro de logs

    :param programa: Nombre del programa para log de errores.
    :type programa: string

    :param nfile: Nombre de archivo con path completo.
    :type nfile: string

    :param dic_data: Diccionario a devolver. No hay verificación de tipos,
                      debe ser un diccionario, no una lista variable de
                      argumentos.
    :type dic_data: dict

    :param agregaFecha:
        En caso de recibir un ``True``, guarda con campo clave ``01_Fecha:``
        la fecha de grabación.
    :type agregaFecha: bool

    :returns: ``True`` o ``False`` según haya podido guardar o no el json
    """

    # --- Para pasar la función
    def mi(datos, archivo):
        json.dump(datos, archivo, ensure_ascii=False, indent=4, sort_keys=True)

    file = nfile + EXT
    funct = mi
    return guardar_archivo_texto(funct, programa, file, dic_data, agregaFecha)


#
def dict_json(unDicc: dict, sort: bool = True, ind: int = 4) -> dict:
    """
    :Propósito:
        Transformar un diccionario Python en un string json, ordenadas las
        claves y con indentación de 4 caracteres por defecto.

    :param unDicc: Diccionario o lista Python
    :type unDicc: ``dict`` / ``list``

    :returns: json formateado
    """
    return json.dumps(unDicc, ensure_ascii=False, sort_keys=sort, indent=ind)


#
def json_dict(unJson: str) -> dict:
    """
    :Propósito: Transformar un json a un diccionario Python.

    :param unJson: Cadena json
    :type unJson: str

    :returns: Diccionario Python
    """
    return json.loads(unJson)


#
class EnteJson(EnteDatos):
    """
    :Propósito:
        Manejar un ente json en memoria de forma abstracta e integral. Este
        objeto se ha definido como una abstracción pura, para ser heredado y
        utilizado por cualquier otro objeto que necesite manejar un ente json
        con estructura fija y permanencia en memoria y/o disco.

        Depende completamente de ``EnteDatos``.
    """

    __slots__ = []

    # --- Parte agregada al diccionario manejador 'self.PAQUETE'.
    FILE = auto()   # --- FILE en disco

    def __init__(self):

        EnteDatos.__init__(self)

        # --- Agregar al diccionario los campos propios
        self.EstablecerCTRL(self.FILE, False)

    #
    def LeerRegistro(self) -> None:
        """ Carga del path self.PAQUETE[ self.REG ] o carga el prototipo. """
        ret = self.DevolverCTRL(self.ENTE)     # --- Objeto que invoca.
        dic_data = dict()
        ret = leer_archivo_json(programa=ret,
                                nfile=self.DevolverCTRL(self.FILE),
                                dic_data=dic_data)

        if ret:
            # --- Sí se logró leer
            self.Agregar(dic_data)

        else:
            # --- No existía, tomamos un registro prototipo
            self.Inicializar()

        # --- Ya no lo necesitamos
        del ret

    #
    def GuardarRegistro(self, agregaFecha: bool = True) -> bool:
        """
        Guarda en el path self.PAQUETE[ self.REG ].

        :param agregaFecha:
            En caso de recibir un ``True``, guarda con campo clave `01_Fecha:``
            la fecha de grabación.
        :type agregaFecha: bool

        :returns: Devuelve un ``True`` si se ha logrado guardar con éxito
        """
        # --- Sólo si tiene un FILE
        aux = self.DevolverCTRL(self.FILE)
        if aux:
            aux = guardar_archivo_json(self.DevolverCTRL(self.ENTE), aux,
                                       self.DevolverTodoElREG(),
                                       agregaFecha=agregaFecha)

            if aux:
                self.EstablecerCTRL(self.GUARDA, True)

            return True

        # --- Si no tenía path, no guardó
        else:
            return False

    #
    @property
    def getJson(self):
        """ Ofrece los datos REG en forma de paquete json. """
        return dict_json(self.DevolverTodoElREG())
