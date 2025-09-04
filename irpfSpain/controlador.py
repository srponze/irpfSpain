from irpfSpain.modelo.modelo import Modelo
from irpfSpain.vista.vista import Vista


class Controlador:

    def __init__(self):

        while True:
            self.modelo = Modelo()
            self.vista = Vista(self)

            self.vista.mostrarMenuPrincipal()

            self.modelo.realizarCalculos()
            datos = self.modelo.obtenerDatos()
            self.vista.enviarDatos(datos)

            self.vista.mostrarResultados()

    def comprobarTransactions(self):
        return self.modelo.comprobarTransactions()

    def comprobarAccount(self):
        return self.modelo.comprobarAccount()

    def comprobarAñoRenta(self, añoRenta: str):
        return self.modelo.comprobarAñoRenta(añoRenta)
