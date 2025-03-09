"""
Configuración global para pytest
"""
import pytest

def pytest_configure(config):
    """Configuración inicial de pytest"""
    config.addinivalue_line(
        "markers",
        "slow: marca tests que son lentos de ejecutar"
    )

@pytest.fixture(autouse=True)
def setup_timeout():
    """Fixture para establecer timeout en todos los tests"""
    pytest.timeout = 5  # 5 segundos máximo por test