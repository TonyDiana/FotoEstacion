#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores globales de cadenas YAML.
    :Autor:     Tony Diana
    :Versión:   28.02.22

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import yaml


# --- Módulos estandard
from . import datos as d
from .datos import auto


# --- Módulos de terceros
from terceros.tinydb import Storage


# --- Extensión de los archivos
EXT = ".yaml"


#
def graba_yaml_general(datos, archivo):
    """ Grabación genérica de yaml. """
    yaml.dump(datos, archivo, encoding='utf-8', allow_unicode=True)


#
def leer_archivo_yaml(programa: str, nfile: str, dic_data: dict,
                      eliminaFecha: bool = True) -> bool:
    """
    :Propósito: Leer un archivo yaml del disco.

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
    funct = yaml.safe_load      # --- Función efectiva
    return d.leer_archivo_texto(funct, programa, file, dic_data, eliminaFecha)


#
def guardar_archivo_yaml(progr: str, nfile: str, dic_data: dict,
                         agregaFecha: bool = True) -> bool:
    """
    :Propósito: Guardar un archivo yaml en disco. Si hay error produce mensaje
                 en el registro de logs

    :param progr: Nombre del programa para log de errores.
    :type progr: string

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
    file = nfile + EXT
    funct = graba_yaml_general
    return d.guardar_archivo_texto(funct, progr, file, dic_data, agregaFecha)


#
def dict_yaml(unDicc: dict) -> dict:
    """
    :Propósito: Transformar un diccionario Python en un string yaml.

    :param unDicc: Diccionario o lista Python
    :type unDicc: ``dict`` / ``list``

    :returns: yaml formateado
    """
    return yaml.dump(unDicc, encoding='utf-8', allow_unicode=True)


#
def yaml_dict(unYaml: str) -> dict:
    """
    :Propósito: Transformar un yaml a un diccionario Python.

    :param unYaml: Cadena yaml
    :type unYaml: str

    :returns: Diccionario Python
    """
    return yaml.safe_load(unYaml)


#
class EnteYaml(d.EnteDatos):
    """
    :Propósito:
        Manejar un ente yaml en memoria de forma abstracta e integral. Este
        objeto se ha definido como una abstracción pura, para ser heredado y
        utilizado por cualquier otro objeto que necesite manejar un ente json
        con estructura fija y permanencia en memoria y/o disco.

        Depende completamente de ``EnteDatos``.
    """

    __slots__ = []

    # --- Parte agregada al diccionario manejador 'self.PAQUETE'.
    FILE = auto()   # --- FILE en disco

    def __init__(self):

        d.EnteDatos.__init__(self)

        # --- Agregar al diccionario los campos propios
        self.EstablecerCTRL(self.FILE, False)

    #
    def LeerRegistro(self) -> None:
        """ Carga del path self.PAQUETE[ self.REG ] o la base prototipo. """
        _ret = self.DevolverCTRL(self.ENTE)     # --- Objeto que invoca.
        _dic_data = dict()
        _ret = leer_archivo_yaml(programa=_ret,
                                 nfile=self.DevolverCTRL(self.FILE),
                                 dic_data=_dic_data)

        if _ret:
            # --- Sí se logró leer
            self.Agregar(_dic_data)

        else:
            # --- No existía, tomamos un registro prototipo
            self.Inicializar()

        # --- Ya no lo necesitamos
        del _ret

    #
    def GuardarRegistro(self, agregaFecha: bool = True) -> bool:
        """
        Guarda en el path el self.PAQUETE[ self.REG ].

        :param agregaFecha:
            En caso de recibir un ``True``, guarda con campo clave
            ``01_Fecha:`` la fecha de grabación.
        :type agregaFecha: bool

        :returns: Devuelve un ``True`` si se ha logrado guardar con éxito
        """
        # --- Sólo si tiene un FILE
        aux = self.DevolverCTRL(self.FILE)
        if aux:
            aux = guardar_archivo_yaml(self.DevolverCTRL(self.ENTE), aux,
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
    def getYaml(self):
        """ Ofrece los datos REG en forma de paquete yaml. """
        return dict_yaml(self.DevolverTodoElREG())


#
class YAMLStorage(Storage):
    """ :Propósito: Manejar registros ``YAML`` para BD ``TinyDB``. """
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            with open(self.filename) as handle:
                data = yaml.safe_load(handle.read())
                return data

        except Exception:
            return None

    def write(self, data):
        with open(self.filename, 'w+') as handle:
            graba_yaml_general(data, handle)

    def close(self):
        pass
