from inquirer import shortcuts

from .constantes.mensajes import *


class MenuPrincipal:

    def mostrarMenu(self) -> str:
        print(TITULO_PRINCIPAL)
        opcion = shortcuts.list_input(
            message=MENSAJE_OPCIONES,
            choices=OPCIONES_PRINCIPALES,
        )
        return opcion
