
class CuentaJugador:
    def __init__(self):
        self.usuario = None
        self.contrasena = None
        self.historial = {
            'partidas_jugadas': 0,
            'partidas_ganadas': 0,
            'puntuacion_total': 0,
            'precision_disparos': 0.0,
            'tiempo_promedio_partida': 0,
            'barcos_hundidos': {
                'buque': 0,
                'crucero': 0,
                'lancha': 0
            },
            'historial_detallado': []
        }

    def registrar(self, usuario: str, contrasena: str) -> bool:
        if self.usuario is not None:
            return False
        self.usuario = usuario
        self.contrasena = contrasena
        return True

    def cambiarContrasena(self, contrasena_actual: str, nueva_contrasena: str) -> bool:
        if self.contrasena == contrasena_actual:
            self.contrasena = nueva_contrasena
            return True
        return False

    def verHistorial(self) -> dict:
        return self.historial

    def agregarPartida(self, ganada: bool, detalles: dict):
        self.historial['partidas_jugadas'] += 1
        if ganada:
            self.historial['partidas_ganadas'] += 1
        
        # Actualizar estadísticas
        self.historial['puntuacion_total'] += detalles.get('puntos', 0)
        disparos_totales = detalles.get('disparos_totales', 0)
        disparos_acertados = detalles.get('disparos_acertados', 0)
        
        if disparos_totales > 0:
            self.historial['precision_disparos'] = (
                (self.historial['precision_disparos'] * (self.historial['partidas_jugadas'] - 1) +
                (disparos_acertados / disparos_totales) * 100) / self.historial['partidas_jugadas']
            )

        # Actualizar barcos hundidos
        for tipo, cantidad in detalles.get('barcos_hundidos', {}).items():
            self.historial['barcos_hundidos'][tipo] += cantidad

        self.historial['tiempo_promedio_partida'] = (
            (self.historial['tiempo_promedio_partida'] * (self.historial['partidas_jugadas'] - 1) +
            detalles.get('tiempo_partida', 0)) / self.historial['partidas_jugadas']
        )

        self.historial['historial_detallado'].append({
            'resultado': 'Victoria' if ganada else 'Derrota',
            'detalles': detalles
        })