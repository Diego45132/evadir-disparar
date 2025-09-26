import pygame
import sys
from typing import NoReturn

from juego import ControlJuego

def main() -> NoReturn:
    """
    Función principal que inicializa y ejecuta el juego.
    
    Esta función se encarga de:
    1. Inicializar pygame y los sistemas necesarios
    2. Configurar la ventana de juego
    3. Crear y ejecutar el ControlJuego
    4. Gestionar la finalización correcta del juego
    
    Returns
    -------
    NoReturn
        Esta función no retorna, termina el proceso al finalizar
    
    Raises
    ------
    pygame.error
        Si hay un error al inicializar pygame o crear la ventana
    Exception
        Para cualquier otro error no esperado durante la ejecución
    
    """
    try:
        # Inicializar Pygame y sus módulos
        _inicializar_pygame()
        
        # Configurar pantalla principal del juego
        pantalla = _configurar_pantalla()
        
        # Crear y ejecutar el gestor del juego
        juego = ControlJuego(pantalla)
        juego.ejecutar()
        
    except pygame.error as e:
        print(f"Error de Pygame durante la ejecución: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado durante la ejecución: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Asegurar que Pygame se cierre correctamente
        _finalizar_pygame()

def _inicializar_pygame() -> None:
    """
    Inicializa todos los módulos necesarios de Pygame.
    
    Raises
    ------
    pygame.error
        Si falla la inicialización de algún módulo de Pygame
    
    Notes
    -----
    Pygame debe inicializarse antes de crear cualquier superficie o usar sus funciones.
    """
    pygame.init()
    
    # Verificar que Pygame se inicializó correctamente
    if not pygame.get_init():
        raise pygame.error("No se pudo inicializar Pygame correctamente")
    
    print("Pygame inicializado correctamente")

def _configurar_pantalla() -> pygame.Surface:
    """
    Configura y crea la ventana principal del juego.
    
    Returns
    -------
    pygame.Surface
        Superficie principal donde se renderizará el juego
    
    Raises
    ------
    pygame.error
        Si no se puede crear la ventana con las dimensiones especificadas
    
    Notes
    -----
    La resolución 800x600 es adecuada para la mayoría de sistemas y proporciones.
    El cursor del mouse se oculta para una experiencia de juego más inmersiva.
    """
    # Configurar dimensiones de la pantalla
    ancho, alto = 800, 600
    resolucion = (ancho, alto)
    
    # Crear la ventana principal
    pantalla = pygame.display.set_mode(resolucion)
    
    # Verificar que la pantalla se creó correctamente
    if pantalla is None:
        raise pygame.error("No se pudo crear la ventana del juego")
    
    # Configurar título de la ventana
    pygame.display.set_caption("Juego Mejorado - Evita y Dispara")
    
    # Ocultar cursor del mouse para mayor inmersión
    pygame.mouse.set_visible(False)
    
    print(f"Pantalla configurada: {ancho}x{alto}")
    return pantalla

def _finalizar_pygame() -> None:
    """
    Finaliza correctamente todos los sistemas de Pygame.
    
    Esta función asegura que todos los recursos de Pygame se liberen
    adecuadamente, independientemente de cómo termine el juego.
    """
    pygame.quit()
    
    print("Pygame finalizado correctamente")

def _mostrar_mensaje_error(mensaje: str) -> None:
    """
    Muestra un mensaje de error en caso de fallo crítico.
    
    Parameters
    ----------
    mensaje : str
        Mensaje de error a mostrar al usuario
    
    Notes
    -----
    Esta función intenta usar pygame para mostrar el error gráficamente,
    pero si falla, recurre a la consola como respaldo.
    """
    try:
        # Intentar mostrar el error en una ventana gráfica
        pantalla_error = pygame.display.set_mode((600, 200))
        pantalla_error.fill((0, 0, 0))
        
        fuente = pygame.font.Font(None, 36)
        texto_error = fuente.render("Error crítico del juego", True, (255, 0, 0))
        texto_mensaje = pygame.font.Font(None, 24).render(mensaje, True, (255, 255, 255))
        
        pantalla_error.blit(texto_error, (50, 50))
        pantalla_error.blit(texto_mensaje, (50, 100))
        pygame.display.flip()
        
        # Esperar que el usuario cierre la ventana
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    
    except Exception as e:
        # Fallback a la consola si falla la interfaz gráfica
        print(f"Error crítico: {mensaje} / {e}", file=sys.stderr)

if __name__ == "__main__":
    """
    Punto de entrada principal del programa.
    
    Cuando el script se ejecuta directamente (no importado como módulo),
    se llama a la función main() para iniciar el juego.
    
    Notes
    -----
    La verificación __name__ == "__main__" asegura que el juego solo se ejecute
    cuando el archivo es ejecutado directamente, no cuando es importado.
    """
    main()

