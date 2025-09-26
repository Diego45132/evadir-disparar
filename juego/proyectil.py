import pygame

from .vector2d import Vector2D
from .figura import Figura


class Proyectil(Figura):
    """
    Representa un proyectil disparado por el jugador u otros elementos del juego.

    Hereda de la clase Figura y añade funcionalidades específicas para proyectiles:
    movimiento direccional, tiempo de vida limitado y desactivación automática.

    Attributes
    ----------
    velocidad : float
        Velocidad de movimiento del proyectil en píxeles por segundo
    direccion : Vector2D
        Vector unitario que indica la dirección del movimiento
    tiempo_vida : float
        Tiempo restante en segundos antes de que el proyectil se desactive

    Inherited Attributes
    --------------------
    pantalla : pygame.Surface
        Superficie donde se dibuja el proyectil
    posicion : Vector2D
        Posición actual del proyectil
    color : Tuple[int, int, int]
        Color amarillo por defecto (255, 255, 0)
    radio : int
        Radio pequeño por defecto (5 píxeles)
    activo : bool
        Estado de actividad del proyectil

    Examples
    --------
    >>> pantalla = pygame.display.set_mode((800, 600))
    >>> direccion = Vector2D(1, 0)  # Derecha
    >>> proyectil = Proyectil(pantalla, 100, 100, direccion, 400)
    >>> proyectil.actualizar(0.016)  # Actualizar para 16ms (60fps)
    """

    def __init__(self, pantalla: pygame.Surface, x: float, y: float, 
                 direccion: 'Vector2D', velocidad: float = 300):
        """
        Inicializa un nuevo proyectil.

        Parameters
        ----------
        pantalla : pygame.Surface
            Superficie de pygame donde se renderizará el proyectil
        x : float
            Posición horizontal inicial del proyectil
        y : float
            Posición vertical inicial del proyectil
        direccion : Vector2D
            Vector que indica la dirección inicial del movimiento
        velocidad : float, optional
            Velocidad del proyectil en píxeles por segundo (por defecto 300)

        Raises
        ------
        TypeError
            Si los tipos de los parámetros no son los esperados
        ValueError
            Si la velocidad no es positiva

        Notes
        -----
        El proyectil se crea como un círculo amarillo pequeño (radio 5).
        La dirección se normaliza automáticamente para ser un vector unitario.
        """
        if not isinstance(direccion, Vector2D):
            raise TypeError("direccion debe ser una instancia de Vector2D")
        if velocidad <= 0:
            raise ValueError("La velocidad debe ser un valor positivo")

        # Inicializar como figura amarilla pequeña
        super().__init__(pantalla, x, y, (255, 255, 0), 5)
        
        self.velocidad = float(velocidad)
        self.direccion = direccion.normalizar()  # Vector unitario
        self.tiempo_vida = 2.0  # segundos

    def actualizar(self, dt: float) -> None:
        """
        Actualiza el estado del proyectil en cada frame del juego.

        Realiza las siguientes operaciones:
        1. Mueve el proyectil en su dirección actual
        2. Reduce el tiempo de vida restante
        3. Desactiva el proyectil si sale de pantalla o se acaba el tiempo

        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos (delta time)

        Raises
        ------
        ValueError
            Si dt no es un valor positivo

        Examples
        --------
        >>> proyectil.actualizar(0.016)  # Para 60 FPS (1/60 ≈ 0.016s)
        >>> # El proyectil se moverá: distancia = 300 * 0.016 = 4.8 píxeles
        """
        if dt <= 0:
            raise ValueError("dt debe ser un valor positivo")

        # Solo procesar si el proyectil está activo
        if not self.activo:
            return

        # 1. Movimiento del proyectil
        movimiento = self.direccion * (self.velocidad * dt)
        self.posicion = self.posicion + movimiento

        # 2. Reducir tiempo de vida
        self.tiempo_vida -= dt

        # 3. Verificar condiciones de desactivación
        self._verificar_desactivacion()

    def _verificar_desactivacion(self) -> None:
        """
        Verifica si el proyectil debe ser desactivado por condiciones del juego.

        Las condiciones de desactivación son:
        - Sale de los límites de la pantalla
        - Se agota el tiempo de vida
        - Ya estaba desactivado previamente

        Notes
        -----
        Este método es llamado automáticamente por actualizar().
        """
        if not self.activo:
            return

        ancho_pantalla = self.pantalla.get_width()
        alto_pantalla = self.pantalla.get_height()

        # Verificar si sale de los límites de la pantalla
        fuera_de_pantalla = (
            self.posicion.x < -self.radio or 
            self.posicion.x > ancho_pantalla + self.radio or
            self.posicion.y < -self.radio or 
            self.posicion.y > alto_pantalla + self.radio
        )

        # Verificar tiempo de vida agotado
        tiempo_agotado = self.tiempo_vida <= 0

        # Desactivar si se cumple alguna condición
        if fuera_de_pantalla or tiempo_agotado:
            self.activo = False

    def __repr__(self) -> str:
        """
        Representación oficial del proyectil para depuración.

        Returns
        -------
        str
            Cadena que representa el estado actual del proyectil
        """
        estado = "activo" if self.activo else "inactivo"
        return (f"Proyectil(pos=({self.x:.1f}, {self.y:.1f}), "
                f"dir=({self.direccion.x:.2f}, {self.direccion.y:.2f}), "
                f"vel={self.velocidad}, vida={self.tiempo_vida:.2f}s, {estado})")

    def __str__(self) -> str:
        """
        Representación legible del proyectil para usuarios.

        Returns
        -------
        str
            Descripción simplificada del proyectil
        """
        return f"Proyectil en ({int(self.x)}, {int(self.y)}) - {self.tiempo_vida:.1f}s restantes"

