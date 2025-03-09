import pytest
from src.game.juego import Juego
from src.game.jugador import Jugador
from src.game.barco import Barco
import time

@pytest.fixture
def juego():
    return Juego()

@pytest.fixture
def juego_con_jugadores():
    juego = Juego()
    jugador1 = Jugador("Jugador1")
    jugador2 = Jugador("Jugador2")
    
    jugador1.registrar("user1", "pass1")
    jugador2.registrar("user2", "pass2")
    
    juego.agregarJugador(jugador1)
    juego.agregarJugador(jugador2)
    return juego

@pytest.fixture
def juego_preparado(juego_con_jugadores):
    """Juego con jugadores y barcos colocados"""
    tipos = ["buque", "buque", "crucero", "crucero", "crucero", "lancha", "lancha", "lancha"]
    for i, tipo in enumerate(tipos):
        barco1 = Barco(tipo)
        barco2 = Barco(tipo)
        juego_con_jugadores.jugadores[0].posicionarBarcos(barco1, 0, i, "vertical")
        juego_con_jugadores.jugadores[1].posicionarBarcos(barco2, 0, i, "vertical")
    
    juego_con_jugadores.iniciarJuego()
    return juego_con_jugadores

def test_agregar_jugador(juego):
    """Caso normal: Agregar jugadores al juego"""
    assert juego.agregarJugador(Jugador("Test1"))
    assert juego.agregarJugador(Jugador("Test2"))
    assert not juego.agregarJugador(Jugador("Test3"))  # Caso de error: Tercer jugador

def test_iniciar_juego_sin_jugadores(juego):
    """Caso de error: Iniciar juego sin jugadores"""
    assert not juego.iniciarJuego()

def test_iniciar_juego_un_jugador(juego):
    """Caso de error: Iniciar juego con un solo jugador"""
    juego.agregarJugador(Jugador("Test1"))
    assert not juego.iniciarJuego()

def test_iniciar_juego_sin_barcos(juego_con_jugadores):
    """Caso de error: Iniciar juego sin barcos colocados"""
    assert not juego_con_jugadores.iniciarJuego()

def test_iniciar_juego_exitoso(juego_preparado):
    """Caso normal: Inicio exitoso del juego"""
    assert juego_preparado.turnoActual is not None
    assert juego_preparado.tiempo_inicio_partida is not None

@pytest.mark.parametrize("x,y,esperado", [
    (0, 0, True),    # Caso normal: Disparo válido
    (10, 10, False), # Caso extremo: Fuera del tablero
    (-1, -1, False), # Caso extremo: Coordenadas negativas
])
def test_realizar_disparo(juego_preparado, x, y, esperado):
    """Pruebas parametrizadas para disparos"""
    assert juego_preparado.realizarDisparo(x, y) == esperado

def test_disparo_fuera_tiempo(juego_preparado, monkeypatch):
    """Caso extremo: Disparo fuera del tiempo límite"""
    # Simular que ha pasado el tiempo límite
    tiempo_futuro = time.time() + 30
    monkeypatch.setattr(time, 'time', lambda: tiempo_futuro)
    
    assert not juego_preparado.realizarDisparo(0, 0)

def test_cambiar_turno(juego_preparado):
    """Caso normal: Cambio de turno"""
    jugador_inicial = juego_preparado.turnoActual
    juego_preparado.cambiarTurno()
    assert juego_preparado.turnoActual != jugador_inicial
    
    # Verificar que el tiempo de inicio del turno se actualiza
    assert juego_preparado.turnoActual.tiempo_inicio_turno is not None

def test_terminar_juego_sin_ganador(juego_preparado):
    """Caso normal: Terminar juego sin ganador"""
    assert juego_preparado.terminarJuego() is None

def test_terminar_juego_con_ganador(juego_preparado):
    """Caso normal: Terminar juego con ganador"""
    # Hundir todos los barcos del jugador 2
    for barco in juego_preparado.jugadores[1].barcos:
        for x, y in barco.posiciones:
            juego_preparado.realizarDisparo(x, y)
    
    ganador = juego_preparado.terminarJuego()
    assert ganador == juego_preparado.jugadores[0]

def test_obtener_estado_juego(juego_preparado):
    """Caso normal: Obtener estado del juego"""
    estado = juego_preparado.obtenerEstadoJuego()
    
    assert estado['turno_actual'] is not None
    assert estado['tiempo_partida'] >= 0
    assert len(estado['jugadores']) == 2
    
    for jugador_estado in estado['jugadores']:
        assert 'nombre' in jugador_estado
        assert 'disparos_restantes' in jugador_estado
        assert 'puntuacion' in jugador_estado
        assert 'precision' in jugador_estado