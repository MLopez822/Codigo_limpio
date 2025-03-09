class Mapa:
    def __init__(self):
        self.tablero = [[' ' for _ in range(10)] for _ in range(10)]
        self.barcos = []
        self.disparos_totales = 0
        self.disparos_acertados = 0

    def colocarBarco(self, barco, x: int, y: int, orientacion: str) -> bool:
        if len(self.barcos) >= 8:
            return False

        try:
            barco.agregarPosicion(x, y, orientacion)
            # Verificar si las posiciones son válidas
            for pos_x, pos_y in barco.posiciones:
                if not (0 <= pos_x < 10 and 0 <= pos_y < 10):
                    return False
                if self.tablero[pos_x][pos_y] != ' ':
                    return False

            # Colocar el barco en el tablero
            for pos_x, pos_y in barco.posiciones:
                self.tablero[pos_x][pos_y] = 'B'
            
            self.barcos.append(barco)
            return True
        except ValueError:
            return False

    def registrarDisparo(self, x: int, y: int, impacto: bool):
        if not (0 <= x < 10 and 0 <= y < 10):
            raise IndexError("Coordenadas fuera del tablero")
            
        self.disparos_totales += 1
        if impacto:
            self.disparos_acertados += 1
        self.tablero[x][y] = 'X' if impacto else 'O'

    def verificarVictoria(self) -> bool:
        return all(barco.hundido for barco in self.barcos)

    def obtenerEstadisticas(self) -> dict:
        precision = 0.0
        if self.disparos_totales > 0:
            precision = (self.disparos_acertados / self.disparos_totales) * 100.0
            
        return {
            'precision': precision,
            'disparos_totales': self.disparos_totales,
            'disparos_acertados': self.disparos_acertados
        }