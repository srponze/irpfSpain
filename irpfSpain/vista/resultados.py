from typing import DefaultDict, Deque, List, Tuple

from inquirer import shortcuts

from ..modelo.entidades.movimiento import Movimiento
from ..modelo.entidades.transaccion import Transaccion
from .constantes.constantes import *
from .constantes.mensajes import *
from .impresora import Impresora


class Resultados:

    def __init__(self):
        self.impresora = Impresora()

    def mostrarComprobacionErrores(
        self,
        listaMovimientosSinCompraActivos: List[Movimiento],
        listaMovimientosSinCompraDivisas: List[Movimiento],
    ):
        print(TITULO_RESULTADOS)
        if listaMovimientosSinCompraActivos:
            print(MENSAJE_ERRORES_MOVIMIENTOS_ACTIVOS)
        if listaMovimientosSinCompraDivisas:
            print(MENSAJE_ERRORES_MOVIMIENTOS_DIVISAS)
        print(SEPARACION)

    def mostrarMenu(self) -> str:
        return shortcuts.list_input(
            message=MENSAJE_OPCIONES_RESULTADOS,
            choices=OPCIONES_RESULTADOS,
        )

    def movimientos(
        self,
        tituloMovimientos: str,
        mensajeCabecera: str,
        listaMovimientos: List[Movimiento],
        codigoImpresion: int,
        tituloPosiciones: str,
        listaPosiciones: DefaultDict[Tuple, Deque[Movimiento]],
        listaMovimientosSinCompra: List[Movimiento],
    ) -> str:

        print(tituloMovimientos)
        print(mensajeCabecera)
        self.impresora.imprimirMovimientos(listaMovimientos, codigoImpresion)

        if listaPosiciones:
            print(tituloPosiciones)
            print(mensajeCabecera)
            self.impresora.imprimirPosiciones(listaPosiciones, codigoImpresion)

        if listaMovimientosSinCompra:
            print(TITULO_VENTAS_SIN_COMPRA_PREVIA)
            print(mensajeCabecera)
            self.impresora.imprimirMovimientos(
                listaMovimientosSinCompra, codigoImpresion
            )
        print()
        return shortcuts.list_input(
            message=MENSAJE_OPCIONES,
            choices=OPCIONES_AUXILIARES_RESULTADOS,
        )

    def transacciones(
        self,
        tituloTransacciones: str,
        mensajeCabecera: str,
        transacciones: DefaultDict[Tuple, List[Transaccion]],
        codigoImpresion: int,
    ) -> str:
        print(tituloTransacciones)
        print(mensajeCabecera)
        self.impresora.imprimirTransacciones(transacciones, codigoImpresion)
        print()
        return shortcuts.list_input(
            message=MENSAJE_OPCIONES,
            choices=OPCIONES_AUXILIARES_RESULTADOS,
        )
