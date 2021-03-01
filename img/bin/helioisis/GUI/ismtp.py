#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Ubicar todos los objetos que sirven para enviar i-mails a elementos
        del menú y evitar las referencias circulares
    :Autor:     Tony Diana
    :Versión:   A8.1

    ---------------------------------------------------------------------------
"""

# --- Módulos estandard
from std.ismtp import ClassMail


#
class MailMain(ClassMail):
    """
    :Propósito: Clase para enviar i-mails al menú/main.

    :param adonde: Opción del menú que deseamos que se ejecute.
    :type adonde: int

    :param auto: Si el mail es auto-iMail. Por defecto no.
    :type auto: bool

    :param send: Si enviar inmediatamente.
    :type auto: bool
    """

    __slots__ = []

    # --- Cuerpo del i-Mail
    __adonde = "ad"     # --- A cual opción de menu ir

    #
    def __init__(self, adonde=False, auto=False, send=False):

        # --- 1º montamos el mail sin enviar todavía
        ClassMail.__init__(self)

        # --- Identidad
        aux = __name__ + "." + self.__class__.__name__
        self.EstablecerCTRL(self.ENTE, aux)
        del aux

        # --- Registro prototipo
        self.MontarPROTO(
            {
                # --- Por defecto nada
                self.__adonde: None,
            })

        # --- Actuar
        self.Actuar(adonde=adonde, auto=auto, send=send)

    #
    # --- Métodos públicos
    #
    #
    def Actuar(self, adonde=False, auto=False, send=False):
        """ Actuar con los parámetros. """
        if adonde:
            self.adonde = adonde

        if auto:
            self.AutoMail()

        if send:
            self.EnviarMail()

    #
    # --- Respuestas
    #
    #
    @property
    def adonde(self):
        """ Obtener / Establecer a dónde se debe dirigir. """
        return self.DevolverREG(self.__adonde)

    @adonde.setter
    def adonde(self, valor):
        self.EstablecerREG(self.__adonde, valor)


#
class MailSetup(MailMain):
    """
    :Propósito: Clase para enviar i-mails al menú/setup.

    :param adonde: Opción del menú que deseamos que se ejecute.
    :type adonde: int

    :param auto: Si el mail es auto-iMail. Por defecto no.
    :type auto: bool

    :param send: Si enviar inmediatamente.
    :type auto: bool
    """

    __slots__ = []

    #
    def __init__(self, adonde=False, auto=False, send=False):

        # --- 1º montamos el mail sin nada más
        MailMain.__init__(self)

        # --- Identidad
        aux = __name__ + "." + self.__class__.__name__
        self.EstablecerCTRL(self.ENTE, aux)
        del aux

        # --- Actuar
        self.Actuar(adonde=adonde, auto=auto, send=send)
