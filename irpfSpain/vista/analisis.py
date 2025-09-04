from typing import Callable, List, Literal

from inquirer import shortcuts

from irpfSpain.vista.constantes.mensajes import *


class Analisis:

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrarMenu(self) -> bool:
        print(TITULO_ANALISIS)
        print(MENSAJE_COMPROBACIONES)

        retorno = self.__pasoDocumento(
            self.controlador.comprobarTransactions,
            MENSAJE_ERRORES_TRANSACTIONS,
            MENSAJE_TRANSACTIONS,
            MENSAJE_OPCIONES,
            OPCIONES_ANALISIS,
        )
        if retorno == False:
            return False

        retorno = self.__pasoDocumento(
            self.controlador.comprobarAccount,
            MENSAJE_ERRORES_ACCOUNT,
            MENSAJE_ACCOUNT,
            MENSAJE_OPCIONES,
            OPCIONES_ANALISIS,
        )
        if retorno == False:
            return False

        retorno = self.__pasoEntradaTexto(
            self.controlador.comprobarAñoRenta,
            MENSAJE_ERRORES_AÑO_RENTA,
            MENSAJE_AÑO_RENTA,
            MENSAJE_OPCIONES,
            OPCIONES_ANALISIS,
            PREGUNTA_AÑO_RENTA,
        )

        if retorno == False:
            return False

        return True

    def __pasoDocumento(
        self,
        funcionComprobar: Callable,
        mensajeErrores: str,
        mensajeCorrecto: str,
        mensajeOpciones: str,
        listaOpciones: List[str],
    ) -> Literal[False] | None:
        while True:
            listaErrores = funcionComprobar()
            if listaErrores:
                print(mensajeErrores)
                for error in listaErrores:
                    print(f" - {error}")
                print()
                opcion = shortcuts.list_input(
                    message=mensajeOpciones, choices=listaOpciones
                )

                if opcion == listaOpciones[1]:
                    return False

            else:
                print(mensajeCorrecto)
                break

    def __pasoEntradaTexto(
        self,
        funcionComprobar: Callable,
        mensajeErrores: str,
        mensajeCorrecto: str,
        mensajeOpciones: str,
        listaOpciones: List[str],
        pregunta: str,
    ) -> Literal[False] | None:
        while True:
            entradaTexto = shortcuts.text(pregunta)
            listaErrores = funcionComprobar(entradaTexto)
            if listaErrores:
                print(mensajeErrores)
                for error in listaErrores:
                    print(f" - {error}")
                    print()
                opcion = shortcuts.list_input(
                    message=mensajeOpciones, choices=listaOpciones
                )

                if opcion == listaOpciones[1]:
                    return False

            else:
                print(mensajeCorrecto)
                break
