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
        super().__init__(pantalla, x, y, (255, 255, 0), 8)
        
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
    
    def pintar(self) -> None:
        """
        Dibuja el proyectil como un misil realista en la pantalla.
        
        Override del método pintar de la clase base para dibujar un misil
        que apunta en la dirección de movimiento con detalles realistas.
        """
        if self.activo:
            x = int(self.posicion.x)
            y = int(self.posicion.y)
            radio = self.radio
            
            # Colores para el misil
            color_principal = self.color  # Amarillo
            color_secundario = tuple(max(0, c - 50) for c in self.color)  # Amarillo oscuro
            color_detalle = tuple(max(0, c - 100) for c in self.color)  # Naranja
            
            # Calcular dirección del misil basada en la dirección de movimiento
            if self.direccion.magnitud() > 0:
                # Normalizar dirección para obtener ángulo
                dir_normalizada = self.direccion.normalizar()
                
                # Cuerpo principal del misil (elipse alargada)
                cuerpo_longitud = radio * 2
                cuerpo_ancho = radio
                
                # Calcular posición del cuerpo
                centro_x = x - int(dir_normalizada.x * radio//2)
                centro_y = y - int(dir_normalizada.y * radio//2)
                
                # Dibujar cuerpo del misil
                pygame.draw.ellipse(self.pantalla, color_principal,
                                  (centro_x - cuerpo_longitud//2, centro_y - cuerpo_ancho//2,
                                   cuerpo_longitud, cuerpo_ancho))
                
                # Punta del misil (cono)
                punta_x = x + int(dir_normalizada.x * radio)
                punta_y = y + int(dir_normalizada.y * radio)
                
                # Base del cono (perpendicular a la dirección)
                perp_x = -dir_normalizada.y * radio // 3
                perp_y = dir_normalizada.x * radio // 3
                
                base1_x = x - int(perp_x)
                base1_y = y - int(perp_y)
                base2_x = x + int(perp_x)
                base2_y = y + int(perp_y)
                
                # Dibujar punta
                puntos_punta = [(punta_x, punta_y), (base1_x, base1_y), (base2_x, base2_y)]
                pygame.draw.polygon(self.pantalla, color_secundario, puntos_punta)
                
                # Cola del misil (estabilizadores)
                cola_x = x - int(dir_normalizada.x * radio)
                cola_y = y - int(dir_normalizada.y * radio)
                
                # Estabilizadores laterales
                estab_x1 = cola_x - int(perp_x * 2)
                estab_y1 = cola_y - int(perp_y * 2)
                estab_x2 = cola_x + int(perp_x * 2)
                estab_y2 = cola_y + int(perp_y * 2)
                
                pygame.draw.line(self.pantalla, color_detalle, 
                                (cola_x, cola_y), (estab_x1, estab_y1), 3)
                pygame.draw.line(self.pantalla, color_detalle, 
                                (cola_x, cola_y), (estab_x2, estab_y2), 3)
                
                # Detalle central en el cuerpo
                pygame.draw.line(self.pantalla, color_detalle,
                                (centro_x - cuerpo_longitud//4, centro_y),
                                (centro_x + cuerpo_longitud//4, centro_y), 2)
            else:
                # Fallback: misil simple si no hay dirección
                pygame.draw.ellipse(self.pantalla, color_principal,
                                  (x - radio, y - radio//2, radio*2, radio))
                pygame.draw.circle(self.pantalla, color_secundario, (x + radio//2, y), radio//3)

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

