import copy
from collections import defaultdict, deque
from typing import DefaultDict, Deque, List, Tuple

from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.entidades.transaccion import Transaccion
from irpfSpain.modelo.fifo.estrategia import Estrategia


class EstrategiaActivos(Estrategia):

    def crearDiccionarios(self) -> None:
        self.transacciones: DefaultDict[Tuple[str, str], List[Transaccion]] = (
            defaultdict(list)
        )
        self.posiciones: DefaultDict[Tuple[str, str], Deque[Movimiento]] = defaultdict(
            deque
        )

    def obtencionCompraOVenta(self, entrada: Movimiento) -> bool:
        return entrada.numero > 0

    def introducirPosicion(self, entrada: Movimiento) -> None:
        self.posiciones[(entrada.isin, entrada.bolsa)].appendleft(entrada)

    def obtencionDeque(self, entrada: Movimiento) -> Deque[Movimiento]:
        return self.posiciones[(entrada.isin, entrada.bolsa)]

    def condicionPositiva(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return entrada.numero + compra.numero < 0

    def transaccionPositiva(self, compra: Movimiento, entrada: Movimiento) -> None:

        transmision = copy.deepcopy(entrada)
        transmision.numero = -compra.numero
        transmision.comision = (
            transmision.comision * transmision.numero / entrada.numero
        )
        super().recalcularMovimiento(transmision)
        transaccion = Transaccion(compra, transmision)

        entrada.numero += compra.numero
        entrada.comision -= transmision.comision
        super().recalcularMovimiento(entrada)

        self.transacciones[(entrada.isin, entrada.bolsa)].append(transaccion)

    def condicionIgual(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return entrada.numero + compra.numero == 0

    def transaccionIgual(self, compra: Movimiento, entrada: Movimiento) -> None:

        transaccion = Transaccion(compra, entrada)
        self.transacciones[(entrada.isin, entrada.bolsa)].append(transaccion)

    def transaccionNegativa(self, compra: Movimiento, entrada: Movimiento) -> None:

        adquisicion = copy.deepcopy(compra)
        adquisicion.numero = -entrada.numero
        adquisicion.comision = adquisicion.comision * adquisicion.numero / compra.numero
        super().recalcularMovimiento(adquisicion)
        transaccion = Transaccion(adquisicion, entrada)

        compra.numero += entrada.numero
        compra.comision -= adquisicion.comision
        super().recalcularMovimiento(compra)

        self.transacciones[(entrada.isin, entrada.bolsa)].append(transaccion)

    def obtenerTransacciones(
        self, añoRenta: int, listaMovimientos: List[Movimiento]
    ) -> Tuple:
        self.añoRenta = añoRenta

        super().algoritmoFifo(
            listaMovimientos,
        )

        return (
            self.transacciones,
            self.posiciones,
            self.listaMovimientosSinCompra,
        )
