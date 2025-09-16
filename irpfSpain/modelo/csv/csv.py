from typing import List

from ..entidades.movimiento import Movimiento
from .estrategia import Estrategia


class Csv:

    def establecerEstrategia(self, estrategia: Estrategia) -> None:
        self.estrategia = estrategia

    def obtenerMovimientos(self, añoRenta, listaDivisas, Path) -> List[Movimiento]:
        return self.estrategia.obtenerMovimientos(añoRenta, listaDivisas, Path)
