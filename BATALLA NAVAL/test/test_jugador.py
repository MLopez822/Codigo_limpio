import pytest
from src.game.jugador import Jugador
from src.game.barco import Barco

@pytest.fixture
def jugador():
    return Jugador("TestJugador")

@pytest.fixture
def jugador_registrado(jugador):
    jugador.registrar("usuario1", "password123")
    return jugador

def test_registro_exitoso(jugador):
    """Caso normal: Registro exitoso de jugador"""
    assert jugador.registrar("usuario1", "password123")
    assert jugador.cuenta.usuario == "usuario1"

def test_registro_duplicado(jugador_registrado):
    """Caso de error: Intento de registro duplicado"""
    assert not jugador_registrado.registrar("usuario2", "password456")

@pytest.mark.parametrize("usuario,contrasena,esperado", [
    ("usuario1", "password123", True),   # Caso normal: Credenciales correctas
    ("usuario1", "password456", False),  # Caso de error: Contraseña incorrecta
    ("usuario2", "password123", False),  # Caso de error: Usuario incorrecto
    ("", "", False),                     # Caso extremo: Credenciales vacías
])
def test_iniciar_sesion(jugador_registrado, usuario, contrasena, esperado):
    """Pruebas parametrizadas para inicio de sesión"""
    assert jugador_registrado.iniciarSesion(usuario, contrasena) == esperado

def test_cambio_contrasena_exitoso(jugador_registrado):
    """Caso normal: Cambio de contraseña exitoso"""
    assert jugador_registrado.cambiarContrasena("password123", "newpassword")
    assert jugador_registrado.iniciarSesion("usuario1", "newpassword")

def test_cambio_contrasena_invalido(jugador_registrado):
    """Caso de error: Cambio de contraseña con credenciales incorrectas"""
    assert not jugador_registrado.cambiarContrasena("password456", "newpassword")

@pytest.mark.parametrize("tipo,x,y,orientacion,esperado", [
    ("buque", 0, 0, "horizontal", True),    # Caso normal: Posición válida
    ("buque", 0, 7, "horizontal", False),   # Caso extremo: Fuera del tablero horizontal
    ("buque", 7, 0, "vertical", False),     # Caso extremo: Fuera del tablero vertical
    ("crucero", 9, 9, "horizontal", False), # Caso extremo: Esquina del tablero
])
def test_posicionar_barcos(jugador, tipo, x, y, orientacion, esperado):
    """Pruebas parametrizadas para posicionamiento de barcos"""
    barco = Barco(tipo)
    assert jugador.posicionarBarcos(barco, x, y, orientacion) == esperado

def test_limite_barcos(jugador):
    """Caso extremo: Intentar colocar más del máximo de barcos permitidos"""
    for i in range(8):
        barco = Barco("lancha")
        assert jugador.posicionarBarcos(barco, i, 0, "horizontal")
    
    # Intentar colocar un noveno barco
    barco_extra = Barco("lancha")
    assert not jugador.posicionarBarcos(barco_extra, 8, 0, "horizontal")

@pytest.mark.parametrize("x,y,esperado", [
    (0, 0, True),    # Caso normal: Disparo válido
    (10, 10, False), # Caso extremo: Fuera del tablero
    (-1, -1, False), # Caso extremo: Coordenadas negativas
    (5, 5, True),    # Caso normal: Centro del tablero
])
def test_disparar(jugador, x, y, esperado):
    """Pruebas parametrizadas para disparos"""
    assert jugador.disparar(x, y) == esperado

def test_registro_impactos_consecutivos(jugador):
    """Caso normal: Registro de impactos consecutivos"""
    # Tres impactos consecutivos
    for _ in range(3):
        jugador.registrarImpacto(True)
        
    assert jugador.disparos_acertados == 3
    assert jugador.disparos_consecutivos == 3
    
    # Fallo que rompe la racha
    jugador.registrarImpacto(False)
    assert jugador.disparos_consecutivos == 0
    assert jugador.disparos_acertados == 3

def test_limite_disparos(jugador):
    """Caso extremo: Alcanzar el límite de disparos"""
    # Realizar todos los disparos permitidos
    for i in range(10):
        assert jugador.disparar(i, 0)
    
    # Intentar realizar un disparo adicional
    assert not jugador.disparar(0, 1)