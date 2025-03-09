class Barco:
    TIPOS = {
        "buque": {"tamaño": 4, "puntos": 100},
        "crucero": {"tamaño": 2, "puntos": 50},
        "lancha": {"tamaño": 1, "puntos": 25}
    }

    def __init__(self, tipo: str):
        if tipo not in self.TIPOS:
            raise ValueError("Tipo de barco no válido")
        self.tipo = tipo
        self.tamaño = self.TIPOS[tipo]["tamaño"]
        self.puntos = self.TIPOS[tipo]["puntos"]
        self.posiciones = []
        self.hundido = False
        self.impactos_recibidos = 0

    def agregarPosicion(self, x: int, y: int, orientacion: str):
        if orientacion not in ["horizontal", "vertical"]:
            raise ValueError("Orientación inválida")
            
        self.posiciones = []
        if orientacion == "horizontal":
            self.posiciones.extend([(x, y + i) for i in range(self.tamaño)])
        elif orientacion == "vertical":
            self.posiciones.extend([(x + i, y) for i in range(self.tamaño)])

    def recibirImpacto(self, x: int, y: int) -> bool:
        if (x, y) in self.posiciones:
            self.impactos_recibidos += 1
            self.hundido = self.impactos_recibidos >= self.tamaño
            return True
        return False

    def obtenerPuntos(self) -> int:
        return self.puntos if self.hundido else 0