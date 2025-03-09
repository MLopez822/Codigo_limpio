class Mapa:
    def __init__(self):
        self.tablero = [[' ' for _ in range(10)] for _ in range(10)]

    def colocarBarco(self, barco, posiciones: list) -> bool:
        # Verificar si las posiciones están libres
        for x, y in posiciones:
            if not (0 <= x < 10 and 0 <= y < 10) or self.tablero[x][y] != ' ':
                return False

        # Colocar el barco en el tablero
        for x, y in posiciones:
            self.tablero[x][y] = 'B'
        return True

    def registrarDisparo(self, x: int, y: int, impacto: bool):
        if 0 <= x < 10 and 0 <= y < 10:
            self.tablero[x][y] = 'X' if impacto else 'O'

    def verificarVictoria(self) -> bool:
        # Verifica si quedan barcos en el tablero
        return not any('B' in fila for fila in self.tablero)