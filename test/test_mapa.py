import pytest
from src.game.mapa import Mapa
from src.game.barco import Barco

@pytest.fixture
def mapa():
    return Mapa()

@pytest.fixture
def mapa_con_barco(mapa):
    barco = Barco("buque")
    mapa.colocarBarco(barco, 0, 0, "horizontal")
    return mapa

@pytest.mark.parametrize("tipo,x,y,orientacion,esperado", [
    ("buque", 0, 0, "horizontal", True),    # Caso normal: Posición válida
    ("buque", 0, 7, "horizontal", False),   # Caso extremo: Fuera del tablero horizontal
    ("crucero", 8, 0, "vertical", False),   # Caso extremo: Fuera del tablero vertical
    ("lancha", 9, 9, "horizontal", True),   # Caso extremo: Esquina del tablero
])
def test_colocar_barco(mapa, tipo, x, y, orientacion, esperado):
    """Pruebas parametrizadas para colocación de barcos"""
    barco = Barco(tipo)
    assert mapa.colocarBarco(barco, x, y, orientacion) == esperado

def test_colocar_barco_solapado(mapa_con_barco):
    """Caso de error: Intentar colocar barco sobre otro"""
    barco = Barco("crucero")
    assert not mapa_con_barco.colocarBarco(barco, 0, 0, "horizontal")

def test_limite_barcos(mapa):
    """Caso extremo: Colocar máximo número de barcos permitido"""
    for i in range(8):
        barco = Barco("lancha")
        assert mapa.colocarBarco(barco, i, 0, "horizontal")
    
    # Intentar colocar un noveno barco
    barco_extra = Barco("lancha")
    assert not mapa.colocarBarco(barco_extra, 8, 0, "horizontal")

@pytest.mark.parametrize("x,y,impacto,marca_esperada", [
    (0, 0, True, 'X'),   # Caso normal: Impacto
    (0, 0, False, 'O'),  # Caso normal: Agua
    (9, 9, True, 'X'),   # Caso extremo: Esquina del tablero
])
def test_registrar_disparo(mapa, x, y, impacto, marca_esperada):
    """Pruebas parametrizadas para registro de disparos"""
    mapa.registrarDisparo(x, y, impacto)
    assert mapa.tablero[x][y] == marca_esperada

def test_registrar_disparo_fuera_tablero(mapa):
    """Caso de error: Disparo fuera del tablero"""
    with pytest.raises(IndexError):
        mapa.registrarDisparo(10, 10, True)

def test_verificar_victoria_tablero_vacio(mapa):
    """Caso extremo: Verificar victoria en tablero vacío"""
    assert mapa.verificarVictoria()

def test_verificar_victoria_progresiva(mapa_con_barco):
    """Caso normal: Verificación progresiva de victoria"""
    assert not mapa_con_barco.verificarVictoria()
    
    # Hundir el barco gradualmente
    for i in range(4):
        mapa_con_barco.registrarDisparo(0, i, True)
    
    assert mapa_con_barco.verificarVictoria()

@pytest.mark.parametrize("disparos,esperado", [
    ([(0, 0, True), (0, 1, True)], 100.0),      # Caso normal: 100% precisión
    ([(0, 0, False), (0, 1, False)], 0.0),      # Caso extremo: 0% precisión
    ([(0, 0, True), (0, 1, False)], 50.0),      # Caso normal: 50% precisión
    ([], 0.0),                                   # Caso extremo: Sin disparos
])
def test_obtener_estadisticas(mapa, disparos, esperado):
    """Pruebas parametrizadas para estadísticas"""
    for x, y, impacto in disparos:
        mapa.registrarDisparo(x, y, impacto)
    
    estadisticas = mapa.obtenerEstadisticas()
    assert estadisticas['precision'] == esperado
    assert estadisticas['disparos_totales'] == len(disparos)
    assert estadisticas['disparos_acertados'] == sum(1 for _, _, imp in disparos if imp)