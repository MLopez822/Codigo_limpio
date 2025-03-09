from src.game.jugador import Jugador
from src.game.mapa import Mapa
import time

class Juego:
    def __init__(self):
        self.jugadores = []
        self.mapas = []
        self.turnoActual = None
        self.tiempo_inicio_partida = None

    def agregarJugador(self, jugador: Jugador) -> bool:
        if len(self.jugadores) < 2:
            self.jugadores.append(jugador)
            self.mapas.append(Mapa())
            return True
        return False

    def iniciarJuego(self) -> bool:
        if len(self.jugadores) != 2:
            return False
        
        for jugador in self.jugadores:
            if len(jugador.barcos) < 8:
                return False

        self.turnoActual = self.jugadores[0]
        self.tiempo_inicio_partida = time.time()
        self.turnoActual.tiempo_inicio_turno = time.time()
        return True

    def realizarDisparo(self, x: int, y: int) -> bool:
        if not self.turnoActual:
            return False

        tiempo_actual = time.time()
        if (tiempo_actual - self.turnoActual.tiempo_inicio_turno) > self.turnoActual.tiempo_limite_turno:
            return False

        jugador_actual_idx = self.jugadores.index(self.turnoActual)
        jugador_objetivo_idx = (jugador_actual_idx + 1) % 2

        if not self.turnoActual.disparar(x, y):
            return False

        impacto = False
        for barco in self.jugadores[jugador_objetivo_idx].barcos:
            if barco.recibirImpacto(x, y):
                impacto = True
                break

        self.mapas[jugador_actual_idx].registrarDisparo(x, y, impacto)
        self.turnoActual.registrarImpacto(impacto)
        self.cambiarTurno()
        return True

    def cambiarTurno(self):
        jugador_actual_idx = self.jugadores.index(self.turnoActual)
        self.turnoActual = self.jugadores[(jugador_actual_idx + 1) % 2]
        self.turnoActual.tiempo_inicio_turno = time.time()

    def terminarJuego(self) -> Jugador:
        for jugador, mapa in zip(self.jugadores, self.mapas):
            if mapa.verificarVictoria():
                return jugador
        return None

    def obtenerEstadoJuego(self) -> dict:
        tiempo_actual = time.time()
        tiempo_partida = tiempo_actual - self.tiempo_inicio_partida if self.tiempo_inicio_partida else 0

        estado_jugadores = []
        for jugador, mapa in zip(self.jugadores, self.mapas):
            estadisticas = mapa.obtenerEstadisticas()
            estado_jugadores.append({
                'nombre': jugador.nombre,
                'disparos_restantes': jugador.MAX_DISPAROS - len(jugador.disparos),
                'puntuacion': sum(barco.obtenerPuntos() for barco in jugador.barcos),
                'precision': estadisticas['precision']
            })

        return {
            'turno_actual': self.turnoActual.nombre if self.turnoActual else None,
            'tiempo_partida': tiempo_partida,
            'jugadores': estado_jugadores
        }