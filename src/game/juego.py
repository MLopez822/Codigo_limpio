from jugador import Jugador
from mapa import Mapa
from barco import Barco
import time

class Juego:
    def __init__(self, dificultad: str = "normal"):
        self.jugadores = []
        self.mapas = []
        self.turnoActual = None
        self.dificultad = dificultad
        self.tiempo_inicio_partida = None

    def agregarJugador(self, jugador: Jugador) -> bool:
        if len(self.jugadores) < 2:
            jugador.configurar_dificultad(self.dificultad)
            self.jugadores.append(jugador)
            self.mapas.append(Mapa())
            return True
        return False

    def iniciarJuego(self) -> bool:
        if len(self.jugadores) != 2:
            return False
        
        for jugador in self.jugadores:
            if len(jugador.barcos) != 8:
                return False

        self.turnoActual = self.jugadores[0]
        self.tiempo_inicio_partida = time.time()
        self.turnoActual.tiempo_inicio_turno = time.time()
        return True

    def realizarDisparo(self, x: int, y: int) -> bool:
        if not self.turnoActual:
            return False

        # Verificar tiempo límite del turno
        tiempo_actual = time.time()
        if (tiempo_actual - self.turnoActual.tiempo_inicio_turno) > self.turnoActual.tiempo_limite_turno:
            return False

        jugador_actual = self.jugadores.index(self.turnoActual)
        jugador_objetivo = (jugador_actual + 1) % 2

        if not self.turnoActual.disparar(x, y):
            return False