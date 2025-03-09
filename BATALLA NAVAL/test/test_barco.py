import pytest
from src.game.barco import Barco

@pytest.fixture
def barcos():
    return {
        'buque': Barco("buque"),
        'crucero': Barco("crucero"),
        'lancha': Barco("lancha")
    }

def test_creacion_barcos_validos(barcos):
    """Caso normal: Creación de barcos con tipos válidos"""
    assert barcos['buque'].tamaño == 4
    assert barcos['crucero'].tamaño == 2
    assert barcos['lancha'].tamaño == 1
    
    assert barcos['buque'].puntos == 100
    assert barcos['crucero'].puntos == 50
    assert barcos['lancha'].puntos == 25

def test_creacion_barco_tipo_invalido():
    """Caso de error: Creación de barco con tipo inválido"""
    with pytest.raises(ValueError, match="Tipo de barco no válido"):
        Barco("submarino")

def test_agregar_posicion_horizontal(barcos):
    """Caso normal: Agregar posición horizontal"""
    barcos['buque'].agregarPosicion(0, 0, "horizontal")
    assert barcos['buque'].posiciones == [(0, 0), (0, 1), (0, 2), (0, 3)]

def test_agregar_posicion_vertical(barcos):
    """Caso normal: Agregar posición vertical"""
    barcos['crucero'].agregarPosicion(1, 1, "vertical")
    assert barcos['crucero'].posiciones == [(1, 1), (2, 1)]

def test_agregar_posicion_orientacion_invalida(barcos):
    """Caso de error: Orientación inválida"""
    with pytest.raises(ValueError):
        barcos['lancha'].agregarPosicion(0, 0, "diagonal")

@pytest.mark.parametrize("coordenadas,esperado", [
    ((0, 0), True),   # Caso normal: Impacto directo
    ((1, 1), False),  # Caso normal: Fallo
    ((9, 9), False),  # Caso extremo: Borde del tablero
])
def test_recibir_impacto(barcos, coordenadas, esperado):
    """Pruebas parametrizadas para diferentes casos de impacto"""
    barcos['lancha'].agregarPosicion(0, 0, "horizontal")
    assert barcos['lancha'].recibirImpacto(*coordenadas) == esperado

def test_hundimiento_progresivo(barcos):
    """Caso normal: Hundimiento progresivo de un barco"""
    barcos['buque'].agregarPosicion(0, 0, "horizontal")
    
    # Primer impacto
    assert barcos['buque'].recibirImpacto(0, 0)
    assert not barcos['buque'].hundido
    assert barcos['buque'].impactos_recibidos == 1
    
    # Hundimiento completo
    for i in range(1, 4):
        assert barcos['buque'].recibirImpacto(0, i)
    assert barcos['buque'].hundido
    assert barcos['buque'].impactos_recibidos == 4

def test_obtener_puntos_diferentes_estados(barcos):
    """Caso normal: Obtención de puntos en diferentes estados"""
    barcos['crucero'].agregarPosicion(0, 0, "horizontal")
    
    # Sin daño
    assert barcos['crucero'].obtenerPuntos() == 0
    
    # Con daño parcial
    barcos['crucero'].recibirImpacto(0, 0)
    assert barcos['crucero'].obtenerPuntos() == 0
    
    # Hundido
    barcos['crucero'].recibirImpacto(0, 1)
    assert barcos['crucero'].obtenerPuntos() == 50

def test_multiples_impactos_misma_posicion(barcos):
    """Caso extremo: Múltiples impactos en la misma posición"""
    barcos['lancha'].agregarPosicion(0, 0, "horizontal")
    
    assert barcos['lancha'].recibirImpacto(0, 0)  # Primer impacto
    assert not barcos['lancha'].recibirImpacto(0, 0)  # Segundo impacto en misma posición