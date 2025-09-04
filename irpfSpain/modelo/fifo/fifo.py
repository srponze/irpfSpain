from typing import List, Tuple

from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.fifo.estrategia import Estrategia


class Fifo:

    def establecerEstrategia(self, estrategia: Estrategia) -> None:
        self.estrategia = estrategia

    def obtenerTransacciones(
        self, añoRenta: int, listaMovimientos: List[Movimiento]
    ) -> Tuple:
        return self.estrategia.obtenerTransacciones(añoRenta, listaMovimientos)
