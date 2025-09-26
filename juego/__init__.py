"""
Paquete principal del juego Evita y Dispara.

Módulos:
- vector2d: Clase para vectores 2D
- figura: Clase base para figuras del juego
- proyectil: Clase para proyectiles disparados
- jugador: Clase del jugador controlado por mouse
- enemigo: Clase del enemigo que persigue al jugador
- control_juego: Gestor principal del juego
"""

__version__ = "1.0.0"
__author__ = "Club de Computación"

# Importaciones principales para facilitar el acceso
from .vector2d import Vector2D
from .figura import Figura
from .proyectil import Proyectil
from .jugador import Jugador
from .enemigo import Enemigo
from .control_juego import ControlJuego

__all__ = ['Vector2D', 'Figura', 'Proyectil', 'Jugador', 'Enemigo', 'ControlJuego' ]

