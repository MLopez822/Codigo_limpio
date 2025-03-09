class CuentaJugador:
    def __init__(self):
        self.usuario = None
        self.contrasena = None
        
    def registrar(self, usuario: str, contrasena: str) -> bool:
        if self.usuario is None:
            self.usuario = usuario
            self.contrasena = contrasena
            return True
        return False
        
    def cambiarContrasena(self, contrasena_actual: str, nueva_contrasena: str) -> bool:
        if self.contrasena == contrasena_actual:
            self.contrasena = nueva_contrasena
            return True
        return False