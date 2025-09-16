from .movimiento import Movimiento


class Transaccion:

    def __init__(self, adquisicion: Movimiento, transmision: Movimiento):
        self.adquisicion = adquisicion
        self.transmision = transmision

    def __str__(self):
        return f"Adquisición: {self.adquisicion}\n" f"Transmisión: {self.transmision}"
