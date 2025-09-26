from typing import Tuple, Optional, TYPE_CHECKING
import pygame

from .vector2d import Vector2D
from .figura import Figura

if TYPE_CHECKING:
    from jugador import Jugador

class Enemigo(Figura):
    """
    Representa un enemigo que persigue al jugador en el juego.

    Hereda de la clase Figura y añade funcionalidades específicas para enemigos:
    comportamiento de persecución, sistema de vida, invulnerabilidad temporal y efectos visuales.

    Attributes
    ----------
    velocidad : float
        Velocidad de movimiento en píxeles por segundo
    objetivo : Optional[Jugador]
        Referencia al jugador que persigue (puede ser None)
    vida : int
        Puntos de vida actuales del enemigo
    vida_maxima : int
        Puntos de vida máximos del enemigo
    tiempo_invulnerable : float
        Tiempo restante de invulnerabilidad en segundos
    color_original : Tuple[int, int, int]
        Color base del enemigo (se restaura después de la invulnerabilidad)

    Inherited Attributes
    --------------------
    pantalla : pygame.Surface
        Superficie donde se dibuja el enemigo
    posicion : Vector2D
        Posición actual del enemigo
    color : Tuple[int, int, int]
        Color actual del enemigo (puede cambiar durante invulnerabilidad)
    radio : int
        Radio del enemigo (20 píxeles por defecto, personalizable)
    activo : bool
        Estado de actividad del enemigo

    Examples
    --------
    >>> pantalla = pygame.display.set_mode((800, 600))
    >>> jugador = Jugador(pantalla, 400, 300, (0, 0, 255))
    >>> enemigo = Enemigo(pantalla, 100, 100, (255, 0, 0), radio=25)
    >>> enemigo.establecer_objetivo(jugador)
    >>> enemigo.actualizar(0.016)  # Persigue al jugador
    """

    def __init__(self, pantalla: pygame.Surface, x: float, y: float, 
                 color: Tuple[int, int, int], radio: int = 20):
        """
        Inicializa un nuevo enemigo con capacidad de persecución.

        Parameters
        ----------
        pantalla : pygame.Surface
            Superficie de pygame donde se renderizará el enemigo
        x : float
            Posición horizontal inicial del enemigo
        y : float
            Posición vertical inicial del enemigo
        color : Tuple[int, int, int]
            Color RGB del enemigo
        radio : int, optional
            Radio del enemigo en píxeles (por defecto 20)

        Raises
        ------
        TypeError
            Si los tipos de los parámetros no son los esperados
        ValueError
            Si el radio no es un valor positivo

        Notes
        -----
        El valor por defecto de radio (20) mantiene la compatibilidad con el código existente.
        """
        if not isinstance(color, tuple) or len(color) != 3:
            raise TypeError("color debe ser una tupla RGB de 3 elementos")
        if radio <= 0:
            raise ValueError("El radio debe ser un valor positivo")

        super().__init__(pantalla, x, y, color, radio)
        
        self.velocidad = 100.0  # píxeles por segundo
        self.objetivo: Optional['Jugador'] = None
        self.vida = 3  # Vida actual del enemigo
        self.vida_maxima = 3  # Vida máxima del enemigo
        self.tiempo_invulnerable = 0.0  # Tiempo de invulnerabilidad en segundos
        self.color_original = color  # Color base para restaurar después de efectos

    def establecer_objetivo(self, objetivo: 'Jugador') -> None:
        """
        Establece el objetivo que el enemigo debe perseguir.

        Parameters
        ----------
        objetivo : Jugador
            Instancia del jugador que será perseguido

        Raises
        ------
        TypeError
            Si objetivo no es una instancia de Jugador

        Examples
        --------
        >>> enemigo.establecer_objetivo(jugador)
        >>> # El enemigo ahora perseguirá al jugador especificado
        """
        if not hasattr(objetivo, 'posicion') or not hasattr(objetivo, 'activo'):
            raise TypeError("El objetivo debe tener atributos 'posicion' y 'activo'")
        
        self.objetivo = objetivo

    def actualizar(self, dt: float) -> None:
        """
        Actualiza el estado del enemigo en cada frame del juego.

        Realiza las siguientes operaciones:
        1. Actualiza el estado de invulnerabilidad y efectos visuales
        2. Persigue al objetivo si está establecido y activo
        3. Mantiene al enemigo dentro de los límites de la pantalla

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
        Durante la invulnerabilidad, el enemigo parpadea para indicar el estado.
        """
        if dt <= 0:
            raise ValueError("dt debe ser un valor positivo")

        # Solo procesar si el enemigo está activo
        if not self.activo:
            return

        # 1. Actualizar invulnerabilidad y efectos visuales
        self._actualizar_invulnerabilidad(dt)

        # 2. Comportamiento de persecución
        self._perseguir_objetivo(dt)

        # 3. Mantener dentro de los límites de la pantalla
        self.mantener_en_pantalla()

    def _actualizar_invulnerabilidad(self, dt: float) -> None:
        """
        Actualiza el estado de invulnerabilidad y aplica efectos visuales.

        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos

        Notes
        -----
        Durante la invulnerabilidad, el enemigo parpadea entre su color original
        y un color más claro para indicar visualmente el estado.
        """
        if self.tiempo_invulnerable > 0:
            # Reducir tiempo de invulnerabilidad
            self.tiempo_invulnerable -= dt

            # Efecto de parpadeo: cambiar color rápidamente
            if int(self.tiempo_invulnerable * 10) % 2 == 0:
                # Color de invulnerabilidad (más claro)
                self.color = (min(255, self.color_original[0] + 100),
                            min(255, self.color_original[1] + 100),
                            min(255, self.color_original[2] + 100))
            else:
                # Color original
                self.color = self.color_original
        else:
            # Restaurar color original cuando termina la invulnerabilidad
            # self.color = self.color_original
            self.color = (max(0, self.color_original[0] - ((3-self.vida)*75)),
                          max(0, self.color_original[1] - ((3-self.vida)*75)),
                          max(0, self.color_original[2] - ((3-self.vida)*75)))

    def _perseguir_objetivo(self, dt: float) -> None:
        """
        Mueve al enemigo hacia su objetivo si está disponible y activo.

        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos

        Notes
        -----
        El movimiento se calcula normalizando la dirección hacia el objetivo
        y aplicando la velocidad teniendo en cuenta el tiempo transcurrido.
        """
        if self.objetivo and self.objetivo.activo:
            # Calcular dirección hacia el objetivo
            direccion = self.objetivo.posicion - self.posicion
            magnitud = direccion.magnitud()

            # Solo mover si el objetivo está a una distancia significativa
            if magnitud > 0:
                direccion_normalizada = direccion.normalizar()
                movimiento = direccion_normalizada * (self.velocidad * dt)
                self.posicion = self.posicion + movimiento

    def recibir_dano(self) -> bool:
        """
        Aplica daño al enemigo, activando invulnerabilidad temporal.

        Returns
        -------
        bool
            True si se aplicó el daño, False si el enemigo era invulnerable

        Examples
        --------
        >>> if enemigo.recibir_dano():
        >>>     print("Daño aplicado al enemigo")
        >>> else:
        >>>     print("Enemigo era invulnerable")

        Notes
        -----
        El enemigo se vuelve invulnerable por 0.5 segundos después de recibir daño.
        Si la vida llega a 0, el enemigo se desactiva.
        """
        # Solo recibir daño si no es invulnerable
        if self.tiempo_invulnerable <= 0:
            self.vida -= 1
            self.tiempo_invulnerable = 0.5  # 0.5 segundos de invulnerabilidad

            # Verificar si el enemigo fue derrotado
            if self.vida <= 0:
                self.activo = False
                self.vida = 0  # Asegurar que no sea negativo

            return True
        
        return False

    def obtener_estado_vida(self) -> Tuple[int, int, float]:
        """
        Obtiene información sobre el estado de vida del enemigo.

        Returns
        -------
        Tuple[int, int, float]
            (vida_actual, vida_maxima, porcentaje_vida)
            - vida_actual: Puntos de vida actuales
            - vida_maxima: Puntos de vida máximos
            - porcentaje_vida: Porcentaje de vida restante (0.0 a 1.0)

        Examples
        --------
        >>> vida_actual, vida_maxima, porcentaje = enemigo.obtener_estado_vida()
        >>> print(f"Vida: {vida_actual}/{vida_maxima} ({porcentaje*100:.1f}%)")
        """
        porcentaje_vida = self.vida / self.vida_maxima if self.vida_maxima > 0 else 0.0
        return (self.vida, self.vida_maxima, porcentaje_vida)

    def __repr__(self) -> str:
        """
        Representación oficial del enemigo para depuración.

        Returns
        -------
        str
            Cadena que representa el estado actual del enemigo
        """
        estado = "activo" if self.activo else "inactivo"
        objetivo = "con objetivo" if self.objetivo else "sin objetivo"
        invulnerable = f", invulnerable {self.tiempo_invulnerable:.1f}s" if self.tiempo_invulnerable > 0 else ""
        
        return (f"Enemigo(pos=({self.x:.1f}, {self.y:.1f}), "
                f"vida={self.vida}/{self.vida_maxima}, "
                f"radio={self.radio}, {objetivo}{invulnerable}, {estado})")

    def __str__(self) -> str:
        """
        Representación legible del enemigo para usuarios.

        Returns
        -------
        str
            Descripción simplificada del enemigo
        """
        return f"Enemigo en ({int(self.x)}, {int(self.y)}) - Vida: {self.vida}/{self.vida_maxima}"

