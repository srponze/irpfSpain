import csv
from bisect import insort
from collections import defaultdict
from datetime import date, time
from pathlib import Path
from typing import DefaultDict, List, Tuple

from irpfSpain.modelo.csv.constantes.columnas import *
from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.entidades.transaccion import Transaccion


class Funciones:

    @staticmethod
    def prorratearComisiones(listaMovimientos: List[Movimiento]) -> None:

        listaMovProrratear = [listaMovimientos[0]]
        for movimiento in listaMovimientos:
            if round(movimiento.comision, 2) != 0:
                if len(listaMovProrratear) != 1:
                    numeroTotal = sum(mov.numero for mov in listaMovProrratear)
                    comisionAProrratear = listaMovProrratear[0].comision
                    for movProrratear in listaMovProrratear:
                        movProrratear.comision = (
                            comisionAProrratear * movProrratear.numero / numeroTotal
                        )

                listaMovProrratear.clear()
                listaMovProrratear.append(movimiento)
            else:
                listaMovProrratear.append(movimiento)

    @staticmethod
    def obtenerListaDivisas(transactionPath: Path) -> List[str]:
        divisas: set[str] = set()
        with open(transactionPath, newline="") as csvtransactions:
            reader = csv.reader(csvtransactions)
            for row in reader:
                if row[l(T_DIVISA)] != "":
                    divisas.add(row[l(T_DIVISA)])
        return list(divisas)

    @staticmethod
    def borrarMovimientosNoNecesarios(
        listaMovimientos: List[Movimiento],
        transacciones: DefaultDict[Tuple, List[Transaccion]],
        añoRenta: int,
    ) -> None:
        listaMovimientos[:] = [
            mov for mov in listaMovimientos if mov.fecha.year == añoRenta
        ]
        listaMovimientosAñadir: List[Movimiento] = []
        for key in transacciones:
            for transaccion in transacciones[key]:
                if transaccion.adquisicion.fecha.year < añoRenta:
                    listaMovimientosAñadir.append(transaccion.adquisicion)
        pass
        for flujo in listaMovimientosAñadir:
            insort(listaMovimientos, flujo, key=lambda x: (x.fecha, x.hora))

    @staticmethod
    def AgruparActivos(
        transaccionesActivos: DefaultDict[Tuple[str, str], List[Transaccion]],
    ) -> DefaultDict[Tuple[str, str], List[Transaccion]]:

        transaccionesAgrupadas: DefaultDict[Tuple[str, str], List[Transaccion]] = (
            defaultdict(list)
        )

        for key in transaccionesActivos:
            if not transaccionesActivos[key]:
                continue
            isin = transaccionesActivos[key][0].adquisicion.isin
            divisa = transaccionesActivos[key][0].adquisicion.divisa
            bolsa = transaccionesActivos[key][0].adquisicion.bolsa
            activo = transaccionesActivos[key][0].adquisicion.activo
            sumaTotalAdquisiciones = 0
            sumaTotalTransmisiones = 0
            sumaNumeroAdquisiciones = 0
            sumaNumeroTranmisiones = 0
            sumaComisionAdquisiciones = 0
            sumaComisionTransmisiones = 0
            for transaccion in transaccionesActivos[key]:
                sumaTotalAdquisiciones += transaccion.adquisicion.total
                sumaTotalTransmisiones += transaccion.transmision.total
                sumaNumeroAdquisiciones += transaccion.adquisicion.numero
                sumaNumeroTranmisiones += transaccion.transmision.numero
                sumaComisionAdquisiciones += transaccion.adquisicion.comision
                sumaComisionTransmisiones += transaccion.transmision.comision

            transaccion = Transaccion(
                adquisicion=Movimiento(
                    date.today(),
                    time(0, 0),
                    activo=activo,
                    bolsa=bolsa,
                    isin=isin,
                    numero=sumaNumeroAdquisiciones,
                    precio=0,
                    valorLocal=0,
                    valor=0,
                    tipoDeCambio=0,
                    comision=sumaComisionAdquisiciones,
                    total=sumaTotalAdquisiciones,
                    divisa=divisa,
                ),
                transmision=Movimiento(
                    date.today(),
                    time(0, 0),
                    isin=isin,
                    activo=activo,
                    bolsa=bolsa,
                    numero=sumaNumeroTranmisiones,
                    precio=0,
                    valorLocal=0,
                    valor=0,
                    tipoDeCambio=0,
                    comision=sumaComisionTransmisiones,
                    total=sumaTotalTransmisiones,
                    divisa=divisa,
                ),
            )
            transaccionesAgrupadas[(isin, bolsa)] = [transaccion]
        return transaccionesAgrupadas
