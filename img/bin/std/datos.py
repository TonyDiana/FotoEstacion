#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores globales de datos
    :Autor:     Tony Diana
    :Versión:   21.01.22

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
from copy import deepcopy


# --- Módulos estandard
from .disco import mkdir
from .logs import log_ERROR
from .tiempo import now


# --- Constantes propias
KEY_FECHA: str = "01_Fecha"     # --- Para almacenar en los registros


#
def auto(*args, **kwargs) -> int:
    """
    :Propósito:
        El autonumerador de enum genera un problema de funcionamiento cuando se
        realiza una copia profunda de un diccionario Python, esta función, de
        idéntica sintaxis y manejo, resuelve ese problema, ofreciendo un número
        int único cada vez que se invoca.

        Para compatibilizar con esta función de la librería estandard, acepta
        parámetros que no usa.

        .. Advertencia::
            Sólo devuelve letras, no ha sido pensada para que devuelva letras
    """

    # --- Crear numerador
    if not hasattr(auto, "__num_auto"):
        auto.__num_auto: int = 0

    # --- Aumentar numerador
    auto.__num_auto += 1
    return auto.__num_auto


#
class EnteDatos(object):
    """
    :Propósito:
        Manejar un ente de datos en memoria de forma abstracta e integral. Este
        objeto se ha definido como una abstracción pura, para ser heredado y
        utilizado por cualquier otro objeto que necesite manejar un ente de
        datos con estructura fija y permanencia en memoria.
    """

    __slots__ = ["PAQUETE"]

    # --- Cuerpo del diccionario manejador 'self.PAQUETE'. (Uso normal)
    PROTO = auto()      # --- Base o estructura prototipo
    REG = auto()        # --- Datos reales que se graban y tienen estructura
    MEM = auto()        # --- Datos libres de uso, que no se grabarán
    CTRL = auto()       # --- Variables de control

    # --- Contenido de CTRL
    BOOLS = auto()      # --- TUPLA con campos bool o False
    INTS = auto()       # --- TUPLA con campos int
    FLOAT = auto()      # --- TUPLA con campos float
    DESCR = auto()      # --- TUPLA con campos descriptivos
    LEIDO = auto()      # --- Bool indica si se ha leido/cargado
    GUARDA = auto()     # --- Bool que indica si se ha guardado
    ENTE = auto()       # --- Ente en el cual estamos (Para log's)

    #
    def __init__(self):

        # --- Diccionario vacío para recibir datos del hijo
        self.PAQUETE = {
            # --- Tienen que ser diccionarios vacíos
            self.PROTO: {},
            self.REG: {},
            self.MEM: {},

            self.CTRL: {
                self.BOOLS: False,
                self.INTS: False,
                self.FLOAT: False,
                self.DESCR: False,
                self.LEIDO: False,
                self.GUARDA: False,
                self.ENTE: "¿?"
            }
        }

    #
    # --- Adición y normalización de datos
    #
    #
    def Agregar(self, unDicc: dict, limpiarPrototipo: bool = True) -> bool:
        """
            Incorpora un json o diccionario a REG. Además transforma
            todos los campos numéricos en numéricos efectivos, por si hemos
            recibido el json con valores string de ellos (por ejemplo, via web)
            ya que via web sólo se reciben los ``bool`` que son ``True``, así
            que se asegura que los no recibidos sean ``False``. También elimina
            los datos recibidos que no corresponden al registro prototipo.
            Después de todo ello limpia el registro prototipo de valores por
            defecto para liberar memoria.
        """

        # --- Eliminamos los campos descriptivos recibidos y los falsos `False`
        self.SinDescriptivos(unDicc)
        self.FalseOk(unDicc)

        # --- Normalizamos la mezcla de datos antiguos y nuevos
        self.PAQUETE[self.REG].update(unDicc)
        self.NormalizarMI()

        # --- Garantizar boobleanos y numéricos
        self.BoolToBoolMI()
        self.IntToIntMI()
        self.FloatToFloatMI()

        # --- Marcamos que ha sido leido en alguna ocasión, limpiamos y salimos
        self.EstablecerCTRL(self.LEIDO, True)
        if limpiarPrototipo:
            self.LimpiarPROTO()

    #
    def Inicializar(self) -> None:
        """ Toma el registro prototipo y lo copia como datos. """
        self.PAQUETE[self.REG] = deepcopy(self.PAQUETE[self.PROTO])

    #
    def SinDescriptivos(self, unDicc: dict) -> None:
        """
            Eliminar los campos descriptivos que vengan del json, ya que
            si no lo hacemos, si cambiamos de decisión en cuanto a la
            descripción, al existir en el json, nunca nos cambiaría al nuevo
            contenido.
        """
        if self.DESCR in self.PAQUETE:
            # --- Por si se ha guardado un False para indicar que no tiene
            if self.PAQUETE[self.CTRL][self.DESCR]:

                temp = self.PAQUETE[self.CTRL][self.DESCR]

                # --- Permitir usar un string
                if (type(temp) is str):
                    temp = (temp,)    # --- Convertir en tupla

                # --- Ahora podemos iterar siempre
                for x in temp:
                    if (x in unDicc):
                        del unDicc[x]

                del temp

    #
    def Normalizar(self, unDicc: dict) -> None:
        """
            Toma un diccionario y lo normaliza con la base prototipo, añadiendo
            los campos que no existen y eliminando los que sobran.
        """
        _final = deepcopy(self.PAQUETE[self.PROTO])
        _final.update(unDicc)

        # --- No se puede borrar de un diccionario mientras se itera el mismo
        _copia = deepcopy(_final)

        for x in _copia:
            if not(x in self.PAQUETE[self.PROTO]):
                del _final[x]

        # --- Y tenemos cuidado de no perder el puntero
        unDicc.clear()
        unDicc.update(_final)

    #
    def NormalizarMI(self) -> None:
        """ Envía self.PAQUETE[ self.REG ] a normalizar. """
        self.Normalizar(self.PAQUETE[self.REG])

    #
    def FalseOk(self, unDicc: dict) -> None:
        """
            Toma un diccionario y añade todos los campos bool que no se reciben
            con valores ``False``. Esto soluciona los problemas de generación
            de falsos ``True`` en json que llegan via web.
        """
        if self.BOOLS in self.PAQUETE:
            # --- ¿Existe?
            if self.PAQUETE[self.CTRL][self.BOOLS]:

                temp = self.PAQUETE[self.CTRL][self.BOOLS]

                # --- Permitir usar un string
                if (type(temp) is str):
                    temp = (temp,)  # --- Convertir en tupla

                # --- Ahora podemos iterar siempre
                for x in temp:
                    if not(x in unDicc):
                        # --- No existe
                        unDicc[x] = False

                del temp

    #
    def BoolToBool(self, unDicc: dict) -> None:
        """
            Toma un diccionario y se asegura que los campos booleanos no sean
            str.
        """
        self.BoolToStr(unDicc, normal=False)

    #
    def BoolToBoolMI(self) -> None:
        """ Asegura los campos booleanos de self.PAQUETE[ self.REG ]. """
        self.BoolToBool(self.PAQUETE[self.REG])

    #
    def BoolToStr(self, unDicc: dict, normal: bool = True) -> None:
        """ Toma un diccionario y convierte los campos booleanos en str. """
        if self.BOOLS in self.PAQUETE:
            # --- ¿Existe?
            if self.PAQUETE[self.CTRL][self.BOOLS]:

                temp = self.PAQUETE[self.CTRL][self.BOOLS]

                # --- Permitir usar un string
                if (type(temp) is str):
                    temp = (temp,)  # --- Convertir en tupla

                # --- Ahora podemos iterar siempre
                for x in temp:
                    if unDicc[x]:
                        if normal:
                            unDicc[x] = "true"

                        else:
                            unDicc[x] = True

                    else:
                        if normal:
                            unDicc[x] = "false"

                        else:
                            unDicc[x] = False

                del temp

    #
    def IntToInt(self, unDicc: dict) -> None:
        """
            Toma un diccionario y se asegura que los campos int son numéricos.
        """
        self.IntToStr(unDicc, normal=False)

    #
    def IntToIntMI(self) -> None:
        """ Asegura los campos int numéricos de self.PAQUETE[ self.REG ]. """
        self.IntToInt(self.PAQUETE[self.REG])

    #
    def IntToStr(self, unDicc: dict, normal: bool = True) -> None:
        """ Toma un diccionario y convierte los campos int a str. """
        if self.INTS in self.PAQUETE:
            # --- ¿Existe?
            if self.PAQUETE[self.CTRL][self.INTS]:

                temp = self.PAQUETE[self.CTRL][self.INTS]

                # --- Permitir usar un string
                if (type(temp) is str):
                    temp = (temp,)  # --- Convertir en tupla

                # --- Ahora podemos iterar siempre
                for x in temp:
                    if normal:
                        unDicc[x] = str(unDicc[x])

                    else:
                        unDicc[x] = int(unDicc[x])

                del temp

    #
    def FloatToFloat(self, unDicc: dict) -> None:
        """
            Toma un diccionario y se asegura que los campos float son
            numéricos.
        """
        self.FloatToStr(unDicc, normal=False)

    #
    def FloatToFloatMI(self) -> None:
        """ Asegura los campos float de self.PAQUETE[ self.REG ]. """
        self.FloatToFloat(self.PAQUETE[self.REG])

    #
    def FloatToStr(self, unDicc: dict, normal: bool = True) -> None:
        """ Toma un diccionario y convierte los campos float en str. """
        if self.FLOAT in self.PAQUETE:
            # --- ¿Existe?
            if self.PAQUETE[self.CTRL][self.FLOAT]:

                temp = self.PAQUETE[self.CTRL][self.FLOAT]

                # --- Permitir usar un string
                if (type(temp) is str):
                    temp = (temp,)  # --- Convertir en tupla

                # --- Ahora podemos iterar siempre
                for x in temp:
                    if normal:
                        unDicc[x] = str(unDicc[x])

                    else:
                        unDicc[x] = float(unDicc[x])

                del temp

    #
    # --- Manejo del REG
    #
    #
    def EstablecerREG(self, clave: str, dato) -> None:
        """
        Agregar el valor de una clave del registro REG del PAQUETE. Realiza
        una copia profunda y elimina los punteros, si es posible.

        :param clave: Clave del campo a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        try:
            self.PAQUETE[self.REG][clave] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.REG][clave] = dato

    #
    def EstablecerPtrREG(self, clave: str, dato) -> None:
        """
        Agregar un puntero al valor de una clave del registro REG del
        PAQUETE.

        :param clave: Clave del campo a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        self.PAQUETE[self.REG][clave] = dato

    #
    def EliminarREG(self, clave: str):
        """
        Elimina una clave del registro REG.

        :returns: Devuelve el dato si existe o un ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.REG]:
            del self.PAQUETE[self.REG][clave]
            return True

        else:
            return False

    #
    def LimpiarREG(self) -> None:
        """ Limpia todo el contenido del REG. """
        self.PAQUETE[self.REG] = {}

    #
    def DevolverREG(self, clave: str):
        """
        Devolver el valor de una clave del registro REG del PAQUETE.

        :returns: Devuelve el dato si existe o un ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.REG]:
            return self.PAQUETE[self.REG][clave]

        else:
            return False

    #
    def DevolverTodoElREG(self) -> dict:
        """ Devolver todo el registro REG del PAQUETE. """
        return self.PAQUETE[self.REG]

    #
    def MontarREG(self, dato) -> None:
        """
        Montar el registro REG del PAQUETE.

        :param dato: Diccionario con los datos
        :type dato: dict

        :returns: nada.
        """
        try:
            self.PAQUETE[self.REG] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.REG] = dato

    #
    # --- Manejo del MEM
    #
    #
    def MontarMEM(self, dato) -> None:
        """
        Montar el registro MEM del PAQUETE.

        :param dato: Diccionario con los datos
        :type dato: dict

        :returns: nada.
        """
        try:
            self.PAQUETE[self.MEM] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.MEM] = dato

    #
    def EstablecerMEM(self, clave: str, dato) -> None:
        """
        Agregar el valor de una clave del registro MEM del PAQUETE. Realiza
        una copia profunda y elimina los punteros, si es posible.

        :param clave: Clave del campo a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        try:
            self.PAQUETE[self.MEM][clave] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.MEM][clave] = dato

    #
    def EstablecerPtrMEM(self, clave: str, dato) -> None:
        """
        Agregar un puntero al valor de una clave del registro MEM del
        PAQUETE.

        :param clave: Clave del campo a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        self.PAQUETE[self.MEM][clave] = dato

    #
    def DevolverMEM(self, clave: str):
        """
        Devolver el valor de una clave del registro MEM del PAQUETE.

        :returns: Devuelve el dato si existe o un ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.MEM]:
            return self.PAQUETE[self.MEM][clave]

        else:
            return False

    #
    def EliminarMEM(self, clave: str):
        """
        Elimina una clave del registro MEN.

        :returns: Devuelve ``True`` si lo logra o ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.MEM]:
            del self.PAQUETE[self.MEM][clave]
            return True

        else:
            return False

    #
    # --- Manejo del PROTO
    #
    #
    def MontarPROTO(self, dato) -> None:
        """
        Montar el registro PROTO del PAQUETE.

        :param dato: Registro prototipo
        :type dato: multi

        :returns: nada.
        """
        try:
            self.PAQUETE[self.PROTO] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.PROTO] = dato

    #
    def EstablecerPROTO(self, clave: str, dato) -> None:
        """
        Agregar el valor de una clave del registro PROTO del PAQUETE.
        Realiza una copia profunda y elimina los punteros, si es posible.

        :param clave: Clave del campo a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        try:
            self.PAQUETE[self.PROTO][clave] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.PROTO][clave] = dato

    #
    def EstablecerPtrPROTO(self, clave: str, dato) -> None:
        """
        Agregar un puntero al valor de una clave del registro PROTO del
        PAQUETE.

        :param clave: Clave del campo a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        self.PAQUETE[self.PROTO][clave] = dato

    #
    def DevolverPROTO(self, clave: str):
        """
        Devolver el valor de una clave del registro PROTOTIPO del PAQUETE.

        :returns: Devuelve el dato si existe o un ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.PROTO]:
            return self.PAQUETE[self.PROTO][clave]

        else:
            return False

    #
    def EliminarPROTO(self, clave: str):
        """
        Elimina una clave del registro PROTO.

        :returns: Devuelve ``True`` si lo logra o ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.PROTO]:
            del self.PAQUETE[self.PROTO][clave]
            return True

        else:
            return False

    #
    def LimpiarPROTO(self) -> None:
        """ Limpia el contenido del registro prototipo sin eliminarlo. """
        for x in self.PAQUETE[self.PROTO]:
            self.EstablecerPROTO(x, None)

    #
    # --- Manejo del CTRL
    #
    #
    def MontarCTRL(self, dato) -> None:
        """
        Montar el registro CTRL del PAQUETE.

        :param dato: Diccionario con datos
        :type dato: dict

        :returns: nada.
        """
        try:
            self.PAQUETE[self.CTRL] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.CTRL] = dato

    #
    def EstablecerCTRL(self, clave: str, dato) -> None:
        """
        Agrega el valor a una clave de control del PAQUETE. Realiza una
        copia profunda y elimina los punteros, si es posible.

        :param clave: Clave del valor a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        try:
            self.PAQUETE[self.CTRL][clave] = deepcopy(dato)

        except Exception:
            self.PAQUETE[self.CTRL][clave] = dato

    #
    def EstablecerPtrCTRL(self, clave: str, dato) -> None:
        """
        Agrega un puntero al valor a una clave de control del PAQUETE.

        :param clave: Clave del valor a guardar
        :type clave: string

        :param dato: Valor del campo a guardar
        :type dato: multi

        :returns: nada.
        """
        self.PAQUETE[self.CTRL][clave] = dato

    #
    def DevolverCTRL(self, clave: str):
        """
        Devolver el valor de una clave de control del PAQUETE.

        :returns: Devuelve el valor o un ``False``.
        """
        if clave in self.PAQUETE[self.CTRL]:
            return self.PAQUETE[self.CTRL][clave]
        else:
            return False

    #
    def EliminarCTRL(self, clave: str):
        """
        Elimina una clave de control del registro del PAQUETE.

        :returns: Devuelve ``True`` si lo logra o ``False`` si no existe.
        """
        if clave in self.PAQUETE[self.CTRL]:
            del self.PAQUETE[self.CTRL][clave]
            return True

        else:
            return False


#
def leer_archivo_texto(funct, programa: str, nfile: str, dic_data: dict,
                       eliminaFecha: bool = True) -> bool:
    """
    Leer del disco un archivo de texto, con formato indeterminado pero con
    estructura de datos.

    :param funct: Función que realizará la carga efectiva.

    :param programa: Nombre del programa para log de errores.
    :type programa: string

    :param nfile: Nombre de archivo con path completo y CON extensión.
    :type nfile: string

    :param dic_data: Diccionario que recibirá los datos (se trata como puntero)
    :type dic_data: string

    :param eliminaFecha:
        En caso de recibir un ``True``, elimina de la cabecera la fecha de
        generación antes de devolver el json
    :type eliminaFecha: bool

    :returns:
        Devuelve un ``True`` si logra leerlo, y un ``False`` sin no lo logra.

    .. Advertencia::
        No funciona si no se le indica cuál función (json, yaml) debe leer de
        forma efectiva. Pensada para ser invocada por otra función.
    """
    try:
        with open(nfile, 'r') as file:
            try:
                diccionario = funct(file)

                # --- Veamos si hay que quitar la fecha
                if (eliminaFecha and (KEY_FECHA in diccionario)):
                    del diccionario[KEY_FECHA]

                # --- Ya se puede devolver, cuidar el puntero
                dic_data.clear()
                dic_data.update(diccionario)
                return True

            except Exception as e:
                # --- Problemas con la estructura, diccionario vacío
                log_ERROR(programa, leer_archivo_texto.__name__, str(e))
                return False

    except Exception as e:
        # --- Si no existe en disco devolvemos error y un diccionario vacío
        log_ERROR(programa, leer_archivo_texto.__name__, str(e))
        return False


#
def guardar_archivo_texto(funct, programa: str, nfile: str, dic_data: dict,
                          agregaFecha: bool = True) -> bool:
    """
    Guardar un archivo indeterminado en disco. Si hay error produce mensaje
    en el registro de logs

    :param funct: Función que realizará el guardado efectivo.

    :param programa: Nombre del programa para log de errores.
    :type programa: string

    :param nfile: Nombre de archivo con path completo y CON extensión.
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

    .. Advertencia::
        No funciona si no se le indica cuál función (json, yaml) debe leer de
        forma efectiva. Pensada para ser invocada por otra función.
    """
    # --- Crear carpeta si no existe
    mkdir(nfile)

    # --- Verificar si hay que adjuntar la fecha
    if agregaFecha:
        dic_data[KEY_FECHA] = now()

    # --- Grabamos
    with open(nfile, 'w') as file:
        try:
            funct(dic_data, file)

        except Exception as e:
            log_ERROR(programa, guardar_archivo_texto.__name__,
                      (nfile + " >>> " + e)
                      )
            return False

        else:
            return True
