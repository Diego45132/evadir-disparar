from typing import Tuple, Dict, Any
import pygame
import math
import random

from .vector2d import Vector2D
from .figura import Figura


class Moneda(Figura):
    """
    Representa una moneda que aparece como recompensa cuando se elimina un enemigo.

    Hereda de la clase Figura y añade funcionalidades específicas para monedas:
    animación de rotación, efecto de brillo y valor de recompensa.

    Attributes
    ----------
    tipo_mejora : str
        Tipo de mejora que otorga la moneda ('velocidad', 'daño', 'rapidez_disparo', 'puntos')
    valor_mejora : int
        Valor de la mejora que otorga la moneda
    tiempo_vida : float
        Tiempo de vida restante de la moneda en segundos
    tiempo_vida_maximo : float
        Tiempo máximo de vida de la moneda en segundos
    angulo_rotacion : float
        Ángulo actual de rotación para el efecto visual
    velocidad_rotacion : float
        Velocidad de rotación en radianes por segundo

    Inherited Attributes
    --------------------
    pantalla : pygame.Surface
        Superficie donde se dibuja la moneda
    posicion : Vector2D
        Posición actual de la moneda
    color : Tuple[int, int, int]
        Color de la moneda (dorado por defecto)
    radio : int
        Radio de la moneda (15 píxeles por defecto)
    activo : bool
        Estado de actividad de la moneda

    Examples
    --------
    >>> pantalla = pygame.display.set_mode((800, 600))
    >>> moneda = Moneda(pantalla, 400, 300, 5)  # Moneda de 5 puntos
    >>> moneda.actualizar(0.016)  # Actualizar para 16ms
    >>> moneda.pintar()  # Dibujar la moneda con animación
    """

    def __init__(self, pantalla: pygame.Surface, x: float, y: float, 
                 tipo_mejora: str = None, valor_mejora: int = 1):
        """
        Inicializa una nueva moneda con tipo de mejora específico.

        Parameters
        ----------
        pantalla : pygame.Surface
            Superficie de pygame donde se renderizará la moneda
        x : float
            Posición horizontal inicial de la moneda
        y : float
            Posición vertical inicial de la moneda
        tipo_mejora : str, optional
            Tipo de mejora ('velocidad', 'daño', 'rapidez_disparo', 'puntos')
            Si es None, se selecciona aleatoriamente
        valor_mejora : int, optional
            Valor de la mejora que otorga la moneda (por defecto 1)

        Raises
        ------
        TypeError
            Si los tipos de los parámetros no son los esperados
        ValueError
            Si el valor no es un número positivo o el tipo no es válido

        Notes
        -----
        La moneda cambia de color según el tipo de mejora.
        """
        if not isinstance(valor_mejora, int) or valor_mejora <= 0:
            raise ValueError("El valor debe ser un número entero positivo")

        # Tipos de mejoras disponibles
        tipos_disponibles = ['velocidad', 'daño', 'rapidez_disparo', 'puntos']
        
        # Seleccionar tipo aleatorio si no se especifica
        if tipo_mejora is None:
            tipo_mejora = random.choice(tipos_disponibles)
        elif tipo_mejora not in tipos_disponibles:
            raise ValueError(f"Tipo de mejora inválido. Debe ser uno de: {tipos_disponibles}")

        # Colores según el tipo de mejora
        colores_mejoras = {
            'velocidad': (0, 255, 0),      # Verde
            'daño': (255, 0, 0),           # Rojo
            'rapidez_disparo': (0, 0, 255), # Azul
            'puntos': (255, 215, 0)        # Dorado
        }
        
        color = colores_mejoras[tipo_mejora]
        
        super().__init__(pantalla, x, y, color, 15)
        
        self.tipo_mejora = tipo_mejora
        self.valor_mejora = valor_mejora
        self.tiempo_vida_maximo = 10.0  # 10 segundos de vida
        self.tiempo_vida = self.tiempo_vida_maximo
        self.angulo_rotacion = 0.0
        self.velocidad_rotacion = 3.0  # radianes por segundo

    def actualizar(self, dt: float) -> None:
        """
        Actualiza el estado de la moneda en cada frame del juego.

        Realiza las siguientes operaciones:
        1. Actualiza la rotación para el efecto visual
        2. Reduce el tiempo de vida
        3. Desactiva la moneda si se agota su tiempo de vida

        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos

        Raises
        ------
        ValueError
            Si dt no es un valor positivo
        """
        if dt <= 0:
            raise ValueError("dt debe ser un valor positivo")

        if not self.activo:
            return

        # 1. Actualizar rotación
        self.angulo_rotacion += self.velocidad_rotacion * dt
        
        # 2. Reducir tiempo de vida
        self.tiempo_vida -= dt
        
        # 3. Desactivar si se agota el tiempo
        if self.tiempo_vida <= 0:
            self.activo = False

    def pintar(self) -> None:
        """
        Dibuja la moneda con efecto de rotación y brillo.

        Override del método pintar de la clase base para crear un efecto visual
        atractivo que incluye rotación y un efecto de brillo basado en el tiempo de vida.

        Notes
        -----
        La moneda se dibuja como un círculo dorado con un efecto de brillo interno
        que cambia según el ángulo de rotación y el tiempo de vida restante.
        """
        if not self.activo:
            return

        x = int(self.posicion.x)
        y = int(self.posicion.y)
        radio = self.radio

        # Calcular intensidad del brillo basado en el tiempo de vida
        intensidad_brillo = self.tiempo_vida / self.tiempo_vida_maximo
        
        # Color base más intenso según el valor
        if self.valor_mejora >= 5:
            color_base = (255, 255, 0)  # Amarillo brillante para monedas de alto valor
        elif self.valor_mejora >= 3:
            color_base = (255, 215, 0)  # Dorado estándar
        else:
            color_base = (255, 200, 0)  # Dorado más tenue

        # Dibujar el círculo principal de la moneda
        pygame.draw.circle(self.pantalla, color_base, (x, y), radio)
        
        # Dibujar borde de la moneda
        pygame.draw.circle(self.pantalla, (200, 150, 0), (x, y), radio, 2)

        # Efecto de brillo rotatorio
        brillo_x = x + int(math.cos(self.angulo_rotacion) * radio * 0.4)
        brillo_y = y + int(math.sin(self.angulo_rotacion) * radio * 0.4)
        brillo_radio = max(3, int(radio * 0.3 * intensidad_brillo))
        
        # Color del brillo (blanco semi-transparente)
        color_brillo = (255, 255, 255)
        pygame.draw.circle(self.pantalla, color_brillo, (brillo_x, brillo_y), brillo_radio)

        # Efecto de destello adicional
        destello_x = x + int(math.cos(self.angulo_rotacion + math.pi) * radio * 0.2)
        destello_y = y + int(math.sin(self.angulo_rotacion + math.pi) * radio * 0.2)
        destello_radio = max(1, int(radio * 0.15 * intensidad_brillo))
        
        pygame.draw.circle(self.pantalla, color_brillo, (destello_x, destello_y), destello_radio)

        # Mostrar el símbolo de la mejora
        simbolos_mejoras = {
            'velocidad': 'V',
            'daño': 'D', 
            'rapidez_disparo': 'R',
            'puntos': 'P'
        }
        
        simbolo = simbolos_mejoras.get(self.tipo_mejora, '?')
        fuente = pygame.font.Font(None, 16)
        texto_mejora = fuente.render(simbolo, True, (0, 0, 0))
        texto_rect = texto_mejora.get_rect(center=(x, y))
        self.pantalla.blit(texto_mejora, texto_rect)

    def recolectar(self) -> Dict[str, Any]:
        """
        Marca la moneda como recolectada y retorna información sobre la mejora.

        Returns
        -------
        Dict[str, Any]
            Diccionario con información de la mejora:
            - 'tipo': tipo de mejora
            - 'valor': valor de la mejora
            - 'puntos': puntos adicionales (solo para tipo 'puntos')

        Examples
        --------
        >>> mejora = moneda.recolectar()
        >>> print(f"¡Mejora de {mejora['tipo']} +{mejora['valor']}!")
        """
        self.activo = False
        return {
            'tipo': self.tipo_mejora,
            'valor': self.valor_mejora,
            'puntos': self.valor_mejora if self.tipo_mejora == 'puntos' else 0
        }

    def obtener_tiempo_vida_restante(self) -> float:
        """
        Obtiene el tiempo de vida restante de la moneda.

        Returns
        -------
        float
            Tiempo restante en segundos antes de que la moneda desaparezca
        """
        return max(0.0, self.tiempo_vida)

    def __repr__(self) -> str:
        """
        Representación oficial de la moneda para depuración.

        Returns
        -------
        str
            Cadena que representa el estado actual de la moneda
        """
        estado = "activa" if self.activo else "inactiva"
        tiempo_restante = self.obtener_tiempo_vida_restante()
        
        return (f"Moneda(pos=({self.x:.1f}, {self.y:.1f}), "
                f"tipo={self.tipo_mejora}, valor={self.valor_mejora}, "
                f"tiempo={tiempo_restante:.1f}s, {estado})")

    def __str__(self) -> str:
        """
        Representación legible de la moneda para usuarios.

        Returns
        -------
        str
            Descripción simplificada de la moneda
        """
        return f"Moneda de {self.tipo_mejora} (+{self.valor_mejora}) en ({int(self.x)}, {int(self.y)})"
