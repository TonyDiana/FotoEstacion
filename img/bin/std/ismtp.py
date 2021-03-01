#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Gestionador de correo interno ente las aplicaciones.
        Este módulo ofrece una clase servidor y una clase cliente de SMTP
        interno entre aplicaciones Python, lo que permite comunicarse a
        entes o aplicaciones que no se complementan entre sí, sin necesidad
        de utilizar la base de datos de la aplicación con tal propósito.

        También le permite a una función o un objeto almacenar múltiples datos
        para procesarlos cuando la ejecución vuelva a invocarlos. Estos se
        consideran auto i-Mails.

        No hay límite en el número de i-Mails o auto i-Mails que se pueden
        enviar a un ente.

        Es lo suficientemente flexible como para no requerir dos servidores
        distintos, por ello sólo está diseñada para que exista un único
        i-servidor en toda la aplicación.

        Utiliza la base de datos ``TinyDB``, de manera que puede utilizar un
        archivo en disco para comunicarse entre aplicaciones o puede utilizar
        un archivo en memoria, lo que permite comunicarse sólo a entes de la
        misma aplicación.

        Utiliza esta base de datos con la siguiente estructura de registro:

        - **PARA**: Se convierte en la tabla del destinatario de los mensajes.

        - **KEY**: Tiene una múltiple funcionalidad:

            - Se puede decidir usar una KEY con significado, para lo cual se le
              otorgará un valor conocido. La KEY podrá ser cualquier cosa que
              pueda servir de índice de un ``dict`` Python.

            - En caso de no precisar una KEY, esta puede quedar en blanco.

            - En caso de enviarse un auto i-mail por el própio ente, esta
              recibirá automáticamente el nombre del ente, el cual es
              también la dirección del destinatario. De esa manera los auto
              i-Mails, los cuales sirven para recordar información al regresar
              al objeto o función, son gestionados automáticamente.

        - **ID**:
            Todo mensaje tendrá un ID único generado por el servidor de manera
            secuncial e irrepetible por ejecución; aunque es semi aleatorio, no
            se puede garantizar que no se repita entre ejecuciones.

        - **FECHA**:
            Todo mensaje tendrá la fecha de generación del mismo, la cual
            incluye los microsegundos.

        - **DE**: Identifica al ente que envía el mensaje.

        - **VOLATIL**:
            Campo y palabra reservada que indica que el mensaje es volatil, es
            decir, que si el servidor **iSMTP** debe guardar los datos entre
            ejecuciones, este mensaje en concreto no debe permanecer entre
            ejecuciones (se pierde ante un corte de luz). Sus valores siempre
            serán ``True`` o ``False``.

        - **CUERPO**:
            Cuerpo del mensaje (En Valenciano cos es cuerpo) y palabra
            reservada.
            Será siempre un diccionario json con los valores a comunicar. Para
            unificar el tratamiento de los mensajes, se ofrece una clase de
            nombre ``ClassMail``, la cual se explica más adelante.

        **Posibilidades:**

        En un entorno multi hilo, podrían estar recibiéndose mensajes de
        entes externos a la aplicación, incluso entes no Python (Web,
        controladores numéricos, etc...), por eso se montó toda la estructura
        de comunicación sobre la clase ``EnteJson``, ya que permite
        ofrecer y recoger un archivo **json** sin ningún inconveniente.

        .. note::
           Es imprescindible, como en cualquier comunicación, que exista un
           código conocido y conocer la dirección del destinatario.

        .. Advertencia::
            Dado que este servidor está pensado para comunicación entre
            procesos, maneja los i-mails por el sistema **LIFO**. Es necesario
            especificar que se desea un sistema **FIFO** a la hora de leer.

    :Autor:     Tony Diana

    :Versión:   21.01.21

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
from random import uniform


# --- Módulos de terceros
from terceros.tinydb import Query


# --- Módulos estándard
from .datos import auto, EnteDatos
from .encoders import base10_OtraBase as gen_KEY
from .tinyDB import BD as BDClass
from .tinyDB import Registro
from .tiempo import now


# --- Destinado a convertirse en el objeto manejador del servidor
iSMTP = None


#
class iSever(Registro):
    """
    :Propósito:
        Servidor de correo interno. Debería instanciarse una sóla vez; para
        ello el módulo ofrece una constante ``SMTP`` inicializada como
        ``None``, la cual está pensada para ser utilizada por la aplicación
        central que la precise:

        Para inicial el servidor, puesto que hay que escribir en una global,
        se hace necesario un código parecido a este:

        .. code-block:: Python

            from std import ismtp as IS
            IS.iSMTP = IS.iServer()

        De esta manera ofrecería un servidor centralizado en un sólo objeto
        a lo largo de toda la aplicación.

        .. advertencia::
            Realiza un manejo especial de la clase heredada ``Registro``, no
            confiar en un manejo general. Cambia constantemente de tabla a la
            que apunta, en virtud del i-Mail que debe manejar.

    :param bd:
        Nombre de la base de datos ``TinyDB`` donde se almacenarán los datos,
        o puede no indicarse y todos los datos se almacenarán en memoria.
    :type bd: string

    :param fijar:
        Un bool que indicará si la BD debe respetarse entre ejecuciones. Por
        defecto no lo hace y, en caso de dejarlo de esta manera, la base de
        datos se vaciará al instanciarse el objeto.
    :type bd: bool


    .. note::
        Dispone de un mecanismo de protección, de manera que si se instancia
        más de un objeto en la misma ejecución, no se borrarán los datos.

    .. importante::
        Cuando devuelve un i-mail no lo borra del servidor, de esta manera se
        puede establecer un sencillo pero efectivo protocolo transaccional.
        Es necesario invocar el método específico para borrar el i-mail, al
        cual se recomienda invocarlo cuando los datos estén procesados o a
        salvo.

    .. note::
        No puede funcionar como clase pero aunque no utiliza una estructura
        de diseño **Singleton**, si se instancia más de un objeto de esta
        clase, todos apuntarán a las mismas propiedades de clase.
    """

    __slots__ = []

    # --- Montar un PAQUETE de EnteDatos de clase para Singleton
    __PAQUETE = None

    #
    # --- Datos REG  OJO: NUNCA USAR AUTO, NO FUNCIONA
    #
    #
    __CUERPO = "C"
    __DE = "D"
    __FECHA = "F"
    __VOLATIL = "V"

    #
    # --- Datos MEM
    #
    #
    __NAME = auto()     # --- Nombre del archivo de la base de datos iSMTP
    __FIJAR = auto()    # --- Si debe permanecer tras el reinicio

    # --- Para no repetir ID's.
    __cont = auto()
    __incr = auto()

    #
    def __init__(self, bd: str = False, fijar: bool = False):

        Registro.__init__(self)

        # --- Singleton sin Singleton
        if self.__class__.__PAQUETE:
            # --- nª instancia de ZEUS, puntero local a clase
            self.PAQUETE = self.__class__.__PAQUETE

        else:
            # --- 1ª instancia, puntero clase iniciado
            self.__class__.__PAQUETE = self.PAQUETE

            # --- Registro prototipo
            self.MontarPROTO(
                {
                    self.__CUERPO: {},
                    self.__DE: None,
                    self.__FECHA: None,
                    self.__VOLATIL: True
                })

            #
            # --- Montar PAQUETE MEM
            #
            self.MontarMEM(
                {
                    self.__NAME: bd,
                    self.__FIJAR: fijar,

                    # --- Produce advertencia de criptografía, pero no importa
                    self.__cont: int(uniform(1, 687231)),
                    self.__incr: int(uniform(1, 4213))
                })

            # --- Montar la base de datos
            self.BD = BDClass(self.DevolverMEM(self.__NAME))

            # --- Veamos si tiene persistencia en disco
            if self.DevolverMEM(self.__FIJAR):
                # --- Borrar los que no sean volátiles
                for x in self.BD.Ptr.tables():
                    tabla = self.BD.PtrTabla(x)
                    buscar = Query()
                    tabla.remove(buscar[self.__VOLATIL] == True)
                    # --- Error de flake8 E712, pero es así en tinyDB

            else:
                # --- Eliminar todas las tablas
                self.BD.Ptr.drop_tables()

    #
    # --- Métodos públicos
    #
    #
    #
    def EnviarMail(self, objmsg: object) -> None:
        """ Enviar un i-Mail. Recibe un objeto clase ``ClassMail``. """

        # --- Montar el mensaje
        self.__limpia_id()
        self.EstablecerCTRL(self.TABLA, objmsg.getPara)
        self.LimpiarREG()

        # --- Asignamos una KEY si no hay ninguna
        if not(objmsg.KEY):
            objmsg.KEY = self.GenerarKEY()

        # --- Montamos el cuerpo del mensaje
        self.EstablecerCTRL(self.KEY, objmsg.KEY)

        self.MontarREG(
            {
                self.__FECHA: objmsg.fecha,
                self.__CUERPO: objmsg.cuerpo,
                self.__VOLATIL: objmsg.getVolatil
            })

        x = objmsg.remitente
        if x:
            self.EstablecerREG(self.__DE, x)

        # --- Enviar, pero primero compatibilizar con Registro genérico
        self.GuardarRegistro()

    #
    def RecibirMail(self, objmsg: object, LIFO: bool = True) -> bool:
        """
        Recibir un i-Mail. Recibe un objeto clase ``ClassMail``. Devuelve un
        bool indicando si lo logró o no.
        """
        self.__limpia_id()
        tabla = self.BD.PtrTabla(objmsg.getPara)
        return self.__MontarMail(objmsg, tabla.all(), LIFO=LIFO)

    #
    def BuscarMail(self, objmsg: object, LIFO: bool = True) -> bool:
        """
        Buscar un i-Mail según la KEY del mismo. Devuelve un booleano indicando
        si lo ha logrado o no. Recibe un objeto clase ``ClassMail``.
        """
        self.__limpia_id()
        tabla = self.BD.PtrTabla(objmsg.getPara)
        buscar = Query()

        msg = tabla.search(buscar[self.KEY] == objmsg.KEY)
        return self.__MontarMail(objmsg, msg, LIFO=LIFO)

    #
    def BorrarMail(self, objmsg: object) -> bool:
        """
        Borra un i-Mail según la KEY del mismo. Devuelve un booleano indicando
        si lo ha logrado o no. Recibe un objeto clase ``ClassMail``.
        """
        self.__limpia_id()
        tabla = self.BD.PtrTabla(objmsg.getPara)
        buscar = Query()

        try:
            tabla.remove(buscar[self.KEY] == objmsg.KEY)
            ret = True

        except Exception:
            ret = False

        del tabla, buscar
        return ret

    #
    # --- Propiedades Especiales
    #
    #
    #
    def GenerarKEY(self):
        """ Genera una KEY para el mensaje. """
        x = self.DevolverMEM(self.__cont) + self.DevolverMEM(self.__incr)
        self.EstablecerMEM(self.__cont, x)
        return gen_KEY(x)

    #
    # --- Propiedades / métodos privados
    #
    #
    # --- Limpiar ID del TinyDB, en esta BD es obsoleto
    def __limpia_id(self) -> None:
        self.EstablecerCTRL(self.ID, None)

    #
    # --- Montar el mail de la respuesta
    def __MontarMail(self, objmsg: object, msg: list, LIFO: bool = True):
        if len(msg):

            # --- 1º Ordenar por fecha y determinar cual toca
            reg = sorted(msg, key=lambda k: k[self.__FECHA])

            # --- En la dirección correcta, leer
            reg = msg[LIFO * -1]

            # --- Montar el mail
            objmsg.KEY = reg[self.KEY]
            objmsg.fecha = reg[self.__FECHA]
            objmsg.cuerpo = reg[self.__CUERPO]

            # --- Opcionales
            if self.__DE in reg:
                objmsg.remitente = reg[self.__DE]

            # --- Y acabar
            resp = True
            del reg

        else:
            resp = False

        return resp


#
class ClassMail(EnteDatos):
    """
    :Propósito:
        Clase pensada para heredar y montar con ella el envío de i-mails. Cada
        ente que precise recibir comunicación por iSMTP. generará su propia
        clase, de manera que no se genera un email para recibir, sino una
        plantilla para recibir, de forma normalizada.

        .. Advertencia::
            Esta clase impone que los argumentos se nombren, unque no impone
            el orden en el que deben hacerlo.

    :param de:
        Un str que indica el remitente del mensaje.
    :type de: str

    :param KEY: Key del mensaje.
    :type KEY: str

    :param msg: Diccionario con el mensaje.
    :type KEY: dict

    :param Volat:
        Un bool que indica si el mensaje debe permanecer tras apagar.
    :type Volat: bool

    :param send:
        Un bool que indica si el mensaje debe enviarse nada más iniciar.
    :type send: bool
    """

    __slots__ = ["vol"]

    # --- Agregados a 'CTRL'.
    __ID = auto()
    __KEY = auto()
    __DATA = auto()
    __DE = auto()

    #
    def __init__(self,
                 de: str = False,
                 KEY: str = False,
                 msg: dict = False,
                 volat: bool = True,
                 send: bool = False
                 ):

        EnteDatos.__init__(self)

        # --- Por defecto, al iniciarse toma la fecha del momento
        self.EstablecerFecha()

        # --- Otros datos
        self.idMensaje = None
        self.remitente = de
        self.KEY = KEY
        self.vol = volat

        # --- Veamos si han pasado el mensaje
        if msg:
            self.RecibirCuerpo(msg)

        # --- Y ahora ver si hay que enviar el mensaje
        if send:
            self.EnviarMail()

    #
    # --- Métodos públicos
    #
    #
    #
    def EstablecerFecha(self) -> None:
        """ Establece el AHORA como fecha del mensaje. """
        self.fecha = now(compacta=True)

    #
    def RecibirCuerpo(self, dato: dict) -> None:
        """ Recibe un diccionario con el cuerpo del mensaje. """
        self.Agregar(dato)

    #
    def EnviarMail(self) -> None:
        """ Enviar un i-Mail. """
        iSMTP.EnviarMail(self)

    #
    def AutoMail(self) -> None:
        """ Marcar el i-Mail como propio. """

        # --- No hay que complicarse la vida, si es auto mensaje, la KEY
        #     y el remitente serán la identidad propia del ente
        x = self.getPara
        self.KEY = x
        self.remitente = x
        del x

    #
    def RecibirMail(self, LIFO: bool = True) -> None:
        """ Recibir un i-Mail. """
        return iSMTP.RecibirMail(self, LIFO=LIFO)

    #
    def RecibirMailYBorrar(self, LIFO: bool = True) -> None:
        """ Recibir un i-Mail e inmediatamente lo borra. """
        resp = self.RecibirMail(LIFO=LIFO)
        self.BorrarMail()
        return resp

    #
    def RecibirAutoMail(self) -> None:
        """ Recibir un i-Mail propio o privado. """
        # --- Una maravilla la decisión de esta KEY
        self.KEY = self.getPara
        return self.BuscarMail()

    #
    def BuscarMail(self, LIFO: bool = True) -> None:
        """ Buscar un i-Mail. """
        return iSMTP.BuscarMail(self, LIFO=LIFO)

    #
    def BorrarMail(self) -> None:
        """ Borrar un i-Mail. """
        return iSMTP.BorrarMail(self)

    #
    # --- Propiedades públicas
    #
    #
    #
    @property
    def getPara(self):
        """ Obtener el destinatario del mensaje. """
        return self.DevolverCTRL(self.ENTE)

    #
    @property
    def remitente(self):
        """ Obtener / Establecer el remitente del mensaje. """
        return self.DevolverMEM(self.__DE)

    @remitente.setter
    def remitente(self, dato):
        self.EstablecerMEM(self.__DE, dato)

    #
    @property
    def idMensaje(self):
        """ Obtener / Establecer el ID del mensaje en el iServer. """
        return self.DevolverMEM(self.__ID)

    @idMensaje.setter
    def idMensaje(self, dato):
        self.EstablecerMEM(self.__ID, dato)

    #
    @property
    def fecha(self):
        """ Obtener / Establecer la fecha del mensaje. """
        return self.DevolverMEM(self.__DATA)

    @fecha.setter
    def fecha(self, dato):
        self.EstablecerMEM(self.__DATA, dato)

    #
    @property
    def KEY(self):
        """ Obtener / Establecer la KEY del mensaje. """
        return self.DevolverCTRL(self.__KEY)

    @KEY.setter
    def KEY(self, dato):
        self.EstablecerCTRL(self.__KEY, dato)

    @property
    def getVolatil(self):
        """ Saber si el mensaje es volatil o con persistencia. """
        return self.vol

    @property
    def cuerpo(self):
        """ Obtener / Establecer el cuerpo del mensaje. """
        return self.DevolverTodoElREG()

    @cuerpo.setter
    def cuerpo(self, dato):
        self.Agregar(dato)
