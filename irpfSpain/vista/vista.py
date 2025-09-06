import sys
from typing import Dict

from inquirer import shortcuts

from irpfSpain.vista.analisis import Analisis
from irpfSpain.vista.constantes.mensajes import *
from irpfSpain.vista.resultados import Resultados


class Vista:

    def __init__(self, controlador) -> None:
        self.controlador = controlador
        self.analisis = Analisis(controlador)
        self.resultados = Resultados()

    def mostrarMenuPrincipal(self) -> None:
        while True:
            print(TITULO_PRINCIPAL)
            opcion = shortcuts.list_input(
                message=MENSAJE_OPCIONES,
                choices=OPCIONES_PRINCIPALES,
            )

            if opcion == OPCIONES_PRINCIPALES[0]:
                if self.analisis.mostrarMenu():
                    break
            elif opcion == OPCIONES_PRINCIPALES[1]:
                sys.exit()

    def mostrarResultados(self) -> None:
        while True:
            if not self.resultados.mostrarMenu(self.datos):
                break

    def enviarDatos(self, datos: Dict) -> None:
        self.datos = datos
