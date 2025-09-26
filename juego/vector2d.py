import math
from typing import Union

class Vector2D:
    """
    Una clase para representar y operar con vectores en 2 dimensiones.

    Soporta operaciones aritméticas básicas como suma, resta, multiplicación escalar,
    cálculo de magnitud y normalización.

    Attributes
    ----------
    x : float
        Componente x del vector
    y : float
        Componente y del vector

    Examples
    --------
    >>> v1 = Vector2D(3, 4)
    >>> v2 = Vector2D(1, 2)
    >>> v3 = v1 + v2
    >>> print(v3)
    Vector2D(4.0, 6.0)

    >>> v4 = v1 * 2
    >>> print(v4)
    Vector2D(6.0, 8.0)
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        Inicializa un vector 2D con las componentes x e y.

        Parameters
        ----------
        x : float, optional
            Componente horizontal (por defecto 0)
        y : float, optional
            Componente vertical (por defecto 0)
        """
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """
        Suma dos vectores componente a componente.

        Parameters
        ----------
        other : Vector2D
            Vector a sumar con la instancia actual

        Returns
        -------
        Vector2D
            Nuevo vector resultante de la suma

        Raises
        ------
        TypeError
            Si other no es una instancia de Vector2D
        """
        if not isinstance(other, Vector2D):
            raise TypeError("La operación requiere una instancia de Vector2D")
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """
        Resta dos vectores componente a componente.

        Parameters
        ----------
        other : Vector2D
            Vector a restar con la instancia actual

        Returns
        -------
        Vector2D
            Nuevo vector resultante de la resta
        """
        if not isinstance(other, Vector2D):
            raise TypeError("La operación requiere una instancia de Vector2D")
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """
        Multiplica el vector por un escalar (multiplicación componente a componente).

        Parameters
        ----------
        scalar : int o float
            Escalar por el que multiplicar el vector

        Returns
        -------
        Vector2D
            Nuevo vector escalado

        Raises
        ------
        TypeError
            Si scalar no es numérico
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("El escalar debe ser un valor numérico")
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """
        Permite la multiplicación por escalar por la derecha (scalar * vector).

        Parameters
        ----------
        scalar : int o float
            Escalar por el que multiplicar el vector

        Returns
        -------
        Vector2D
            Nuevo vector escalado
        """
        return self.__mul__(scalar)

    def __repr__(self) -> str:
        """
        Representación oficial del vector para depuración.

        Returns
        -------
        str
            Representación en cadena que puede ser usada para recrear el objeto
        """
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self) -> str:
        """
        Representación legible del vector para usuarios.

        Returns
        -------
        str
            Representación en cadena amigable
        """
        return f"({self.x}, {self.y})"

    def magnitud(self) -> float:
        """
        Calcula la magnitud (longitud) del vector.

        Returns
        -------
        float
            Magnitud del vector según el teorema de Pitágoras

        Examples
        --------
        >>> v = Vector2D(3, 4)
        >>> v.magnitud()
        5.0
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalizar(self) -> 'Vector2D':
        """
        Devuelve un vector unitario en la misma dirección que el vector actual.

        Returns
        -------
        Vector2D
            Vector normalizado de magnitud 1

        Notes
        -----
        Si la magnitud del vector es 0, se devuelve un vector cero para evitar
        divisiones por cero.
        """
        mag = self.magnitud()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)

