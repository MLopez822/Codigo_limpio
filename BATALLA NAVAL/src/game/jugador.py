from src.game.cuenta_jugador import CuentaJugador
from src.game.barco import Barco

class Jugador:
    MAX_BARCOS = 8
    MAX_DISPAROS = 10

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuenta = CuentaJugador()
        self.barcos = []
        self.disparos = []
        self.disparos_acertados = 0
        self.disparos_consecutivos = 0
        self.tiempo_inicio_turno = None
        self.tiempo_limite_turno = 30  # 30 segundos por turno

    def configurar_dificultad(self, dificultad: str):
        if dificultad == "facil":
            self.tiempo_limite_turno = 45
        elif dificultad == "dificil":
            self.tiempo_limite_turno = 15

    def registrar(self, usuario: str, contrasena: str) -> bool:
        return self.cuenta.registrar(usuario, contrasena)

    def iniciarSesion(self, usuario: str, contrasena: str) -> bool:
        return (self.cuenta.usuario == usuario and 
                self.cuenta.contrasena == contrasena)

    def cambiarContrasena(self, contrasena_actual: str, nueva_contrasena: str) -> bool:
        return self.cuenta.cambiarContrasena(contrasena_actual, nueva_contrasena)

    def posicionarBarcos(self, barco: Barco, x: int, y: int, orientacion: str) -> bool:
        if len(self.barcos) >= self.MAX_BARCOS:
            return False

        try:
            barco.agregarPosicion(x, y, orientacion)
            # Verificar si las posiciones son válidas
            for pos_x, pos_y in barco.posiciones:
                if not (0 <= pos_x < 10 and 0 <= pos_y < 10):
                    return False
                # Verificar superposición con otros barcos
                for b in self.barcos:
                    if (pos_x, pos_y) in b.posiciones:
                        return False
            
            self.barcos.append(barco)
            return True
        except ValueError:
            return False

    def disparar(self, x: int, y: int) -> bool:
        if not (0 <= x < 10 and 0 <= y < 10):
            return False
        if len(self.disparos) >= self.MAX_DISPAROS:
            return False
        if (x, y) in self.disparos:
            return False
        
        self.disparos.append((x, y))
        return True

    def registrarImpacto(self, impacto: bool):
        if impacto:
            self.disparos_acertados += 1
            self.disparos_consecutivos += 1
        else:
            self.disparos_consecutivos = 0