#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores personalizados de base de datos TinyDB
    :Autor:     Tony Diana
    :Versión:   21.01.24

    ---------------------------------------------------------------------------
"""


# --- Módulos de terceros
from terceros.tinydb import TinyDB, Query
from terceros.tinydb.operations import delete
from terceros.tinydb.storages import MemoryStorage


# --- Módulos estandard
from .datos import auto, EnteDatos, KEY_FECHA
from .json import EXT as EXT_JSON
from .tiempo import now
from .yaml import EXT as EXT_YAML
from .yaml import YAMLStorage


# --- Constantes del módulo
WORD_KEY = "00_KEY"


#
class BD(object):
    """
    :Propósito: Manejar una base de datos ``TinyDB`` tipo json (por defecto).

    :param file:
        Nombre del archivo SIN EXTENSIÓN, o nada para grabar en memoria.
    :type file: str

    """

    __slots__ = ["Ptr", "nombre"]

    def __init__(self, file: str = False):

        if file:
            # --- Disco
            self.nombre = (file + EXT_JSON)
            self.open()
        else:
            # --- Memoria
            self.nombre = False
            self.Ptr = TinyDB(storage=MemoryStorage)

    #
    # --- Métodos
    #
    #
    #
    #
    def PtrTabla(self, tabla: str, cache: int = 0):
        """
        Devuelve el puntero de una tabla.

        :param tabla: Nombre de la tabla.
        :type tabla: str

        :param cache: Tamaño de la caché, por defecto ninguna (Recomendado).
        :type cache: int
        """
        self.open()
        return self.Ptr.table(tabla, cache_size=cache)

    #
    def close(self) -> None:
        """ Cerrar la base de datos. """
        if self.nombre:
            self.Ptr.close()

    #
    def open(self) -> None:
        """ Abrir la base de datos. """
        if self.nombre:
            self.Ptr = TinyDB(self.nombre, sort_keys=True, indent=4,
                              separators=(',', ': '), ensure_ascii=False)


#
class BDYaml(BD):
    """
    :Propósito: Manejar una base de datos ``TinyDB`` tipo yaml.

    :param file: Nombre del archivo o nada para grabar en memoria.
    :type file: str

    .. nota::
        No tiene sentido usar este objeto en memoria, porque en memoria
        ``TinyDB`` nunca usa ni ``json`` ni ``yaml`` ni otro formato que
        no sea un diccionario Python, pero disponer de la posibilidad permite
        cambiar de tipo en ejecución, además de una estandarización del
        tratamiento.
    """

    __slots__ = ["Ptr", "nombre"]

    def __init__(self, file: str = False):

        BD.__init__(self)

        if file:
            # --- Disco
            self.nombre = (file + EXT_YAML)
            self.open()

    #
    # --- Métodos
    #
    #
    #
    #
    def open(self) -> None:
        """ Abrir la base de datos. """
        if self.nombre:
            self.Ptr = TinyDB(self.nombre, storage=YAMLStorage)


#
class Registro(EnteDatos):
    """
    :Propósito:
        Manejar un registro de una tabla ``TinyDB`` como un ``EnteDatos``.

    :param BD:
        Puntero a la base de datos. Puede montarse después de ``__init__``.
    :type BD: objet
    """

    __slots__ = ["BD"]

    # --- Parte agregada al  diccionario manejador 'self.PAQUETE'

    # --- NO AUTO, VA AL JSON, Clave del registro
    KEY = WORD_KEY
    # --- NO AUTO, VA AL JSON, Clave del registro

    TABLA = auto()      # --- Tabla a la que pertenece
    ID = auto()         # --- Identificador de registro TinyDB en la tabla

    def __init__(self, BD: object = None):

        EnteDatos.__init__(self)

        # --- Puntero a la base de datos
        self.BD = BD

        # --- Agregar al diccionario los campos propios de CTRL
        self.EstablecerCTRL(self.TABLA, False)
        self.EstablecerCTRL(self.KEY, False)
        self.EstablecerCTRL(self.ID, False)

    #
    def AñadirKEY(self):
        """ Añade KEY y fecha de grabación al registro prototipo y memoria. """
        k = self.DevolverCTRL(self.KEY)
        self.EstablecerPROTO(self.KEY, k)

        if k:
            self.EstablecerREG(self.KEY, k)
        del k

        self.EstablecerPROTO(KEY_FECHA, self.DevolverCTRL(KEY_FECHA))

    #
    def LeerRegistro(self) -> None:
        """ Carga de la tabla self.PAQUETE[ self.REG ], o el prototipo. """
        self.BD.open()
        query = Query()
        tabla = self.BD.PtrTabla(self.DevolverCTRL(self.TABLA))

        # --- Si tenemos ID de registro, eso usamos
        if self.DevolverCTRL(self.ID):
            reg = tabla.get(doc_id=self.DevolverCTRL(self.ID))
        else:
            reg = tabla.get(query[self.KEY] == self.DevolverCTRL(self.KEY))

        # --- Añadimos la KEY y fecha de grabado al registro PROTO para REG
        self.AñadirKEY()

        # --- Según sea 1ª vez o ya exista
        if reg:
            self.EstablecerCTRL(self.ID, reg.doc_id)
            self.Agregar(reg)

        else:
            # --- No existía, tomamos un registro prototipo
            self.EstablecerCTRL(self.ID, False)
            self.Inicializar()

        # --- Llevar la KEY a donde falte
        kc = self.DevolverCTRL(self.KEY)
        kr = self.DevolverREG(self.KEY)

        if kc:
            self.EstablecerREG(self.KEY, kc)

        elif kr:
            self.EstablecerCTRL(self.KEY, kr)

        del kr, kc, query, tabla, reg
        self.BD.close()

    #
    def GuardarRegistro(self, masfecha: bool = False) -> bool:
        """
        Guarda en la tabla a self.PAQUETE[ self.REG ].

        :param masfecha:
            Indica si debe agregar la fecha de grabación al registro.
        :type masfecha: bool

        :returns: Devuelve un ``True`` si se ha logrado guardar con éxito.
        """

        # --- Sólo si tiene una tabla y una KEY asociados
        if (self.DevolverCTRL(self.TABLA) and self.DevolverCTRL(self.KEY)):

            self.BD.open()

            # --- Añadimos KEY y fecha de grabado al registro PROTO para REG
            self.AñadirKEY()

            # --- Preparar la tabla
            tabla = self.BD.PtrTabla(self.DevolverCTRL(self.TABLA))

            # --- Y la fecha de grabado, si procede
            if masfecha:
                self.EstablecerREG(KEY_FECHA, now())
            else:
                self.EliminarREG(KEY_FECHA)
                self.EliminarPROTO(KEY_FECHA)

            # --- Ver si tenemos ID (actualizar) o es registro nuevo
            if self.DevolverCTRL(self.ID):
                # --- Ya existe
                tabla.update(self.PAQUETE[self.REG],
                             doc_ids=[self.DevolverCTRL(self.ID)])

                # --- Ahora normalizamos el contenido
                reg = tabla.get(doc_id=self.DevolverCTRL(self.ID))
                for x in reg:
                    if not(x in self.PAQUETE[self.PROTO]):
                        tabla.update(delete(x),
                                     doc_ids=[self.DevolverCTRL(self.ID)])
                del reg

            else:
                # --- Nuevo
                id = tabla.insert(self.PAQUETE[self.REG])
                self.EstablecerCTRL(self.ID, id)
                del id

            # --- Marcar grabado y proceder
            self.PAQUETE[self.CTRL][self.GUARDA] = True
            del tabla

            self.BD.close()

            return True

        # --- Si no tenía datos, no guardó
        else:
            return False

    #
    def BorrarRegistro(self) -> None:
        """ Borra el registro de la base de datos. """
        self.BD.open()
        query = Query()
        tabla = self.BD.PtrTabla(self.DevolverCTRL(self.TABLA))

        # --- Si tenemos ID de registro, eso usamos
        if self.DevolverCTRL(self.ID):
            reg = tabla.remove(doc_ids=(self.DevolverCTRL(self.ID),))
            # --- Se requiere un iterable para los ID's en remove
        else:
            reg = tabla.remove(query[self.KEY] == self.DevolverCTRL(self.KEY))

        del query, tabla, reg
        self.BD.close()
