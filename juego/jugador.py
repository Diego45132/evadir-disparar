from typing import List, Tuple
import pygame

from .vector2d import Vector2D
from .figura import Figura
from .proyectil import Proyectil


class Jugador(Figura):
    """
    Representa al jugador controlado por el mouse en el juego.

    Hereda de la clase Figura y añade funcionalidades específicas para el jugador:
    movimiento suave hacia el cursor, sistema de disparo con cooldown, y gestión de proyectiles.

    Attributes
    ----------
    velocidad_movimiento : float
        Factor de suavizado para el movimiento (0.0 a 1.0)
    ultimo_disparo : float
        Tiempo transcurrido desde el último disparo en segundos
    cooldown_disparo : float
        Tiempo mínimo requerido entre disparos en segundos
    proyectiles : List[Proyectil]
        Lista de proyectiles activos disparados por el jugador

    Inherited Attributes
    --------------------
    pantalla : pygame.Surface
        Superficie donde se dibuja el jugador
    posicion : Vector2D
        Posición actual del jugador
    color : Tuple[int, int, int]
        Color del jugador
    radio : int
        Radio del jugador (20 píxeles por defecto)
    activo : bool
        Estado de actividad del jugador

    Examples
    --------
    >>> pantalla = pygame.display.set_mode((800, 600))
    >>> jugador = Jugador(pantalla, 400, 300, (0, 0, 255))
    >>> jugador.actualizar(0.016)  # Actualizar para 16ms
    >>> jugador.disparar((500, 300))  # Disparar hacia la derecha
    """

    def __init__(self, pantalla: pygame.Surface, x: float, y: float, 
                 color: Tuple[int, int, int]):
        """
        Inicializa un nuevo jugador controlado por mouse.

        Parameters
        ----------
        pantalla : pygame.Surface
            Superficie de pygame donde se renderizará el jugador
        x : float
            Posición horizontal inicial del jugador
        y : float
            Posición vertical inicial del jugador
        color : Tuple[int, int, int]
            Color RGB del jugador

        Raises
        ------
        TypeError
            Si los tipos de los parámetros no son los esperados
        """
        if not isinstance(color, tuple) or len(color) != 3:
            raise TypeError("color debe ser una tupla RGB de 3 elementos")

        # Inicializar como figura con radio 20
        super().__init__(pantalla, x, y, color, 20)
        
        self.velocidad_movimiento = 0.1  # Factor de suavizado del movimiento
        self.ultimo_disparo = 0.0  # Tiempo desde el último disparo
        self.cooldown_disparo = 0.3  # segundos entre disparos
        self.proyectiles: List[Proyectil] = []  # Lista de proyectiles activos

    def actualizar(self, dt: float) -> None:
        """
        Actualiza el estado del jugador en cada frame del juego.

        Realiza las siguientes operaciones:
        1. Movimiento suave hacia la posición del mouse
        2. Mantiene al jugador dentro de los límites de la pantalla
        3. Actualiza el temporizador de cooldown de disparo
        4. Actualiza y gestiona el ciclo de vida de los proyectiles

        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos (delta time)

        Raises
        ------
        ValueError
            Si dt no es un valor positivo

        Notes
        -----
        El movimiento utiliza interpolación lineal para un efecto suave.
        Los proyectiles inactivos se eliminan automáticamente de la lista.
        """
        if dt <= 0:
            raise ValueError("dt debe ser un valor positivo")

        # Solo procesar si el jugador está activo
        if not self.activo:
            return

        # 1. Movimiento suave hacia la posición del mouse
        self._mover_hacia_mouse()

        # 2. Mantener dentro de los límites de la pantalla
        self.mantener_en_pantalla()

        # 3. Actualizar cooldown de disparo
        self.ultimo_disparo += dt

        # 4. Actualizar y gestionar proyectiles
        self._actualizar_proyectiles(dt)

    def _mover_hacia_mouse(self) -> None:
        """
        Mueve al jugador suavemente hacia la posición actual del cursor.

        Utiliza interpolación lineal para un movimiento fluido:
        nueva_pos = pos_actual + (objetivo - pos_actual) * factor

        Notes
        -----
        La velocidad_movimiento controla la suavidad (0.0 = inmóvil, 1.0 = instantáneo).
        """
        pos_mouse = pygame.mouse.get_pos()
        objetivo = Vector2D(pos_mouse[0], pos_mouse[1])
        diferencia = objetivo - self.posicion

        # Aplicar movimiento suavizado
        self.posicion = self.posicion + diferencia * self.velocidad_movimiento

    def _actualizar_proyectiles(self, dt: float) -> None:
        """
        Actualiza todos los proyectiles del jugador y elimina los inactivos.

        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos

        Notes
        -----
        Se usa una copia de la lista para evitar problemas al modificar durante la iteración.
        """
        # Crear copia de la lista para iterar de forma segura
        for proyectil in self.proyectiles[:]:
            proyectil.actualizar(dt)
            if not proyectil.activo:
                self.proyectiles.remove(proyectil)

    def disparar(self, objetivo_pos: Tuple[float, float]) -> bool:
        """
        Dispara un proyectil hacia la posición objetivo especificada.

        Parameters
        ----------
        objetivo_pos : Tuple[float, float]
            Posición (x, y) hacia donde apuntar el disparo

        Returns
        -------
        bool
            True si se realizó el disparo, False si está en cooldown

        Raises
        ------
        TypeError
            Si objetivo_pos no es una tupla de 2 elementos

        Examples
        --------
        >>> jugador.disparar((500, 300))  # Disparar hacia posición (500, 300)
        True  # Disparo exitoso

        >>> jugador.disparar((500, 300))
        False  # En cooldown, no se puede disparar
        """
        if not isinstance(objetivo_pos, tuple) or len(objetivo_pos) != 2:
            raise TypeError("objetivo_pos debe ser una tupla de 2 elementos (x, y)")

        # Verificar cooldown
        if self.ultimo_disparo < self.cooldown_disparo:
            return False

        # Calcular dirección del disparo
        direccion = Vector2D(
            objetivo_pos[0] - self.posicion.x,
            objetivo_pos[1] - self.posicion.y
        )

        # Crear y almacenar nuevo proyectil
        proyectil = Proyectil(self.pantalla, self.posicion.x, self.posicion.y, direccion)
        self.proyectiles.append(proyectil)

        # Reiniciar temporizador de disparo
        self.ultimo_disparo = 0.0

        return True

    def pintar(self) -> None:
        """
        Dibuja al jugador y todos sus proyectiles activos en la pantalla.

        Override del método pintar de la clase base para incluir los proyectiles.

        Notes
        -----
        Primero se dibujan los proyectiles y luego el jugador para mantener
        un orden de renderizado consistente.
        """
        if not self.activo:
            return

        # Pintar proyectiles primero (para que queden detrás del jugador si hay superposición)
        for proyectil in self.proyectiles:
            proyectil.pintar()

        # Luego pintar al jugador
        super().pintar()

    def obtener_estado_disparo(self) -> Tuple[bool, float]:
        """
        Obtiene información sobre el estado del sistema de disparo.

        Returns
        -------
        Tuple[bool, float]
            (puede_disparar, tiempo_restante_cooldown)
            - puede_disparar: True si el jugador puede disparar
            - tiempo_restante_cooldown: Tiempo restante para poder disparar (0 si está listo)

        Examples
        --------
        >>> puede_disparar, tiempo_restante = jugador.obtener_estado_disparo()
        >>> print(f"Puede disparar: {puede_disparar}, Tiempo restante: {tiempo_restante:.2f}s")
        """
        puede_disparar = self.ultimo_disparo >= self.cooldown_disparo
        tiempo_restante = max(0.0, self.cooldown_disparo - self.ultimo_disparo)
        return (puede_disparar, tiempo_restante)

    def __repr__(self) -> str:
        """
        Representación oficial del jugador para depuración.

        Returns
        -------
        str
            Cadena que representa el estado actual del jugador
        """
        estado = "activo" if self.activo else "inactivo"
        puede_disparar, tiempo_restante = self.obtener_estado_disparo()
        estado_disparo = "listo" if puede_disparar else f"cooldown {tiempo_restante:.1f}s"
        
        return (f"Jugador(pos=({self.x:.1f}, {self.y:.1f}), "
                f"proyectiles={len(self.proyectiles)}, "
                f"disparo={estado_disparo}, {estado})")

    def __str__(self) -> str:
        """
        Representación legible del jugador para usuarios.

        Returns
        -------
        str
            Descripción simplificada del jugador
        """
        return f"Jugador en ({int(self.x)}, {int(self.y)}) con {len(self.proyectiles)} proyectiles"

