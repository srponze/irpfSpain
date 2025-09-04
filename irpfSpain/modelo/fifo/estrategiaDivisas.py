import copy
from collections import defaultdict, deque
from typing import Deque, List, Tuple

from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.entidades.transaccion import Transaccion
from irpfSpain.modelo.fifo.estrategia import Estrategia


class EstrategiaDivisas(Estrategia):

    def crearDiccionarios(self) -> None:
        self.transacciones: defaultdict[str, List[Transaccion]] = defaultdict(list)
        self.posiciones: defaultdict[str, Deque[Movimiento]] = defaultdict(deque)

    def obtencionCompraOVenta(self, entrada: Movimiento) -> bool:
        return entrada.valorLocal > 0

    def introducirPosicion(self, entrada: Movimiento):
        self.posiciones[entrada.divisa].appendleft(entrada)

    def obtencionDeque(self, entrada: Movimiento) -> Deque[Movimiento]:
        return self.posiciones[entrada.divisa]

    def condicionPositiva(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return entrada.valorLocal + compra.valorLocal < -0.5

    def transaccionPositiva(self, compra: Movimiento, entrada: Movimiento):

        transmision = copy.deepcopy(entrada)
        transmision.precio = compra.precio
        transmision.comision = (
            transmision.comision * transmision.precio / entrada.precio
        )
        super().recalcularMovimiento(transmision)
        transaccion = Transaccion(compra, transmision)

        entrada.precio -= compra.precio
        entrada.comision -= transmision.comision
        super().recalcularMovimiento(entrada)

        self.transacciones[entrada.divisa].append(transaccion)

    def condicionIgual(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return round(entrada.precio + compra.precio) == 0

    def transaccionIgual(self, compra: Movimiento, entrada: Movimiento) -> None:

        transaccion = Transaccion(compra, entrada)
        self.transacciones[entrada.divisa].append(transaccion)

    def transaccionNegativa(self, compra: Movimiento, entrada: Movimiento) -> None:

        adquisicion = copy.deepcopy(compra)
        adquisicion.precio = entrada.precio
        adquisicion.comision = adquisicion.comision * adquisicion.precio / compra.precio
        super().recalcularMovimiento(adquisicion)
        transaccion = Transaccion(adquisicion, entrada)

        compra.precio -= entrada.precio
        compra.comision -= adquisicion.comision
        super().recalcularMovimiento(compra)

        self.transacciones[entrada.divisa].append(transaccion)

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
