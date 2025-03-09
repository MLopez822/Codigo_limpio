from cuenta_jugador import CuentaJugador
from barco import Barco

class Jugador:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuenta = None
        self.barcos = []
        self.disparos = []

    def registrar(self, usuario: str, contrasena: str):
        self.cuenta = CuentaJugador(usuario, contrasena)

    def iniciarSesion(self, usuario: str, contrasena: str) -> bool:
        return (self.cuenta and 
                self.cuenta.usuario == usuario and 
                self.cuenta.contrasena == contrasena)

    def cambiarContrasena(self, nueva_contrasena: str):
        if self.cuenta:
            self.cuenta.cambiarContrasena(nueva_contrasena)

    def posicionarBarcos(self, barco: Barco, posiciones: list) -> bool:
        # Verificar si las posiciones son válidas
        for x, y in posiciones:
            if not (0 <= x < 10 and 0 <= y < 10):
                return False
            # Verificar si hay superposición con otros barcos
            for b in self.barcos:
                if any((x, y) in b.posiciones for x, y in posiciones):
                    return False

        for x, y in posiciones:
            barco.agregarPosicion(x, y)
        self.barcos.append(barco)
        return True

    def disparar(self, x: int, y: int) -> bool:
        if (x, y) in self.disparos:
            return False
        self.disparos.append((x, y))
        return True