import pygame
from typing import Tuple
from .vector2d import Vector2D

class Figura:
    """
    Clase base abstracta para representar figuras circulares en el juego.

    Proporciona funcionalidad básica para renderizado, detección de colisiones
    y gestión de límites de pantalla. Diseñada para ser extendida por clases específicas.

    Attributes
    ----------
    pantalla : pygame.Surface
        Superficie donde se dibujará la figura
    posicion : Vector2D
        Posición central de la figura en coordenadas 2D
    color : Tuple[int, int, int]
        Color RGB de la figura
    radio : int
        Radio del círculo que representa la figura
    activo : bool
        Estado que determina si la figura debe ser procesada y dibujada

    Examples
    --------
    >>> pantalla = pygame.display.set_mode((800, 600))
    >>> figura = Figura(pantalla, 100, 100, (255, 0, 0), 25)
    >>> figura.pintar()  # Dibuja un círculo rojo en (100, 100)
    """

    def __init__(self, pantalla: pygame.Surface, x: float, y: float, 
                 color: Tuple[int, int, int], radio: int = 20):
        """
        Inicializa una nueva figura circular.

        Parameters
        ----------
        pantalla : pygame.Surface
            Superficie de pygame donde se renderizará la figura
        x : float
            Posición horizontal inicial del centro de la figura
        y : float
            Posición vertical inicial del centro de la figura
        color : Tuple[int, int, int]
            Color RGB de la figura (rojo, verde, azul)
        radio : int, optional
            Radio del círculo en píxeles (por defecto 20)

        Raises
        ------
        TypeError
            Si los tipos de los parámetros no son los esperados
        """
        if not isinstance(pantalla, pygame.Surface):
            raise TypeError("pantalla debe ser una instancia de pygame.Surface")
        if not isinstance(color, tuple) or len(color) != 3:
            raise TypeError("color debe ser una tupla RGB de 3 elementos")
        
        self.pantalla = pantalla
        self.posicion = Vector2D(x, y)
        self.color = color
        self.radio = int(radio)
        self.activo = True

    @property
    def x(self) -> float:
        """
        Obtiene la coordenada x de la posición actual.

        Returns
        -------
        float
            Coordenada x del centro de la figura
        """
        return self.posicion.x

    @property
    def y(self) -> float:
        """
        Obtiene la coordenada y de la posición actual.

        Returns
        -------
        float
            Coordenada y del centro de la figura
        """
        return self.posicion.y

    def pintar(self) -> None:
        """
        Dibuja la figura en la pantalla si está activa.

        Utiliza pygame.draw.circle para renderizar un círculo con las propiedades
        actuales de la figura. Solo se dibuja si la figura está marcada como activa.

        Notes
        -----
        Las coordenadas se convierten a enteros para compatibilidad con pygame.
        """
        if self.activo:
            pygame.draw.circle(
                self.pantalla, 
                self.color,
                (int(self.posicion.x), int(self.posicion.y)), 
                self.radio
            )

    def colision(self, otro: 'Figura') -> bool:
        """
        Detecta colisión entre esta figura y otra figura circular.

        Parameters
        ----------
        otro : Figura
            Otra figura con la que verificar colisión

        Returns
        -------
        bool
            True si hay colisión, False en caso contrario

        Notes
        -----
        La colisión se calcula comparando la distancia entre centros con la suma de radios.
        Solo se considera colisión si ambas figuras están activas.

        Examples
        --------
        >>> figura1 = Figura(pantalla, 100, 100, (255,0,0), 20)
        >>> figura2 = Figura(pantalla, 120, 100, (0,0,255), 20)
        >>> figura1.colision(figura2)
        True  # Porque 20px de distancia < 40px (20+20)
        """
        if not (self.activo and otro.activo):
            return False
        
        distancia = (self.posicion - otro.posicion).magnitud()
        return distancia <= (self.radio + otro.radio)

    def mantener_en_pantalla(self) -> None:
        """
        Ajusta la posición para mantener la figura dentro de los límites de la pantalla.

        Evita que la figura se salga de los bordes de la pantalla ajustando su posición
        para que siempre sea completamente visible.

        Notes
        -----
        Considera el radio de la figura para que no se corte en los bordes.
        """
        ancho_pantalla = self.pantalla.get_width()
        alto_pantalla = self.pantalla.get_height()

        # Ajustar posición horizontal
        self.posicion.x = max(self.radio, self.posicion.x)
        self.posicion.x = min(ancho_pantalla - self.radio, self.posicion.x)
        
        # Ajustar posición vertical
        self.posicion.y = max(self.radio, self.posicion.y)
        self.posicion.y = min(alto_pantalla - self.radio, self.posicion.y)

    def actualizar(self) -> None:
        """
        Método de actualización para ser sobrescrito por subclases.

        Esta implementación base no realiza ninguna acción. Las subclases deben
        implementar este método para definir comportamientos específicos como
        movimiento, animación, o cambios de estado.

        Examples
        --------
        class Pelota(Figura):
            def actualizar(self):
                # Lógica específica de actualización para la pelota
                self.posicion.x += 1  # Movimiento horizontal
                self.mantener_en_pantalla()
        """
        pass

