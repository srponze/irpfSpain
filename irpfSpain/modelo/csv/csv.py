from typing import List

from irpfSpain.modelo.csv.estrategia import Estrategia
from irpfSpain.modelo.entidades.movimiento import Movimiento


class Csv:

    def establecerEstrategia(self, estrategia: Estrategia) -> None:
        self.estrategia = estrategia

    def obtenerMovimientos(self, añoRenta, listaDivisas, Path) -> List[Movimiento]:
        return self.estrategia.obtenerMovimientos(añoRenta, listaDivisas, Path)
