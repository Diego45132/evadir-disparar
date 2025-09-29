import random
import pygame
from typing import Optional

from .figura import Figura
from .jugador import Jugador
from .enemigo import Enemigo
from .proyectil import Proyectil

class ControlJuego:
    """
    Gestiona el estado general del juego, coordinando todos los elementos.

    Se encarga de la inicialización, actualización, renderizado y gestión de
    eventos del juego. También maneja la lógica de colisiones, sistema de puntos
    y transiciones de estado (juego activo/game over).

    Attributes
    ----------
    pantalla : pygame.Surface
        Superficie principal donde se renderiza el juego
    puntos : int
        Puntuación actual del jugador
    jugador : Optional[Jugador]
        Instancia del jugador (None hasta inicialización)
    enemigo : Optional[Enemigo]
        Instancia del enemigo (None hasta inicialización)
    fuente : pygame.font.Font
        Fuente para renderizar texto de la interfaz
    clock : pygame.time.Clock
        Reloj para controlar la tasa de refresco del juego
    jugando : bool
        Estado que indica si el juego está en curso
    tiempo_desde_ultimo_dano : float
        Tiempo transcurrido desde el último daño recibido por el jugador
    cooldown_dano : float
        Tiempo mínimo entre daños que puede recibir el jugador

    Examples
    --------
    >>> pantalla = pygame.display.set_mode((800, 600))
    >>> game_manager = ControlJuego(pantalla)
    >>> game_manager.ejecutar()  # Inicia el bucle principal del juego
    """
    def __init__(self, pantalla: pygame.Surface):
        """
        Inicializa el gestor del juego con la superficie de renderizado.

        Parameters
        ----------
        pantalla : pygame.Surface
            Superficie de pygame donde se renderizará el juego

        Raises
        ------
        TypeError
            Si pantalla no es una instancia de pygame.Surface
        """
        if not isinstance(pantalla, pygame.Surface):
            raise TypeError("pantalla debe ser una instancia de pygame.Surface")

        self.pantalla = pantalla
        self.puntos = 10
        self.jugador: Optional[Jugador] = None
        self.enemigo: Optional[Enemigo] = None
        
        # Sistema de niveles
        self.nivel_actual = 1
        self.enemigos_eliminados_nivel = 0
        self.enemigos_para_siguiente_nivel = 3
        
        # Sistema de fuentes para la interfaz de usuario
        self.fuente = pygame.font.Font(None, 36)  # Fuente por defecto, tamaño 36
        self.fuente_pequena = pygame.font.Font(None, 24)  # Fuente para instrucciones
        
        self.clock = pygame.time.Clock()
        self.jugando = True
        self.tiempo_desde_ultimo_dano = 0.0
        self.cooldown_dano = 1.0  # 1 segundo de cooldown para recibir daño
        self.enemigos = []  
        
# ✅ Timers para controlar aparición de enemigos
        self.tiempo_enemigo = 0.0
        self.intervalo_enemigo = 5.0

        # Sistema de fondos por niveles
        self.fondos_nivel = []
        self.cargar_fondos_niveles()
        self.fondo_actual = 0
        self.actualizar_fondo()
        

        # Inicializar el estado del juego
        self.inicializar_juego()
    
    def cargar_fondos_niveles(self) -> None:
        """
        Carga las imágenes de fondo para diferentes niveles.
        
        Intenta cargar múltiples fondos, si no existen usa el fondo por defecto.
        """
        try:
            # Intentar cargar fondos específicos por nivel
            fondos_posibles = [
                "juego/static/fondo_nivel1.png",
                "juego/static/fondo_nivel2.png", 
                "juego/static/fondo_nivel3.png",
                "juego/static/fondo_nivel4.png",
                "juego/static/fondo_nivel5.png"
            ]
            
            for fondo_path in fondos_posibles:
                try:
                    imagen = pygame.image.load(fondo_path).convert()
                    ancho_pantalla = self.pantalla.get_width()
                    alto_pantalla = self.pantalla.get_height()
                    fondo_escalado = pygame.transform.scale(imagen, (ancho_pantalla, alto_pantalla))
                    self.fondos_nivel.append(fondo_escalado)
                except pygame.error:
                    # Si no existe el fondo específico, usar el fondo por defecto
                    imagen = pygame.image.load("juego/static/image.png").convert()
                    ancho_pantalla = self.pantalla.get_width()
                    alto_pantalla = self.pantalla.get_height()
                    fondo_escalado = pygame.transform.scale(imagen, (ancho_pantalla, alto_pantalla))
                    self.fondos_nivel.append(fondo_escalado)
            
            # Si no se cargó ningún fondo, usar el fondo por defecto
            if not self.fondos_nivel:
                imagen = pygame.image.load("juego/static/image.png").convert()
                ancho_pantalla = self.pantalla.get_width()
                alto_pantalla = self.pantalla.get_height()
                fondo_escalado = pygame.transform.scale(imagen, (ancho_pantalla, alto_pantalla))
                self.fondos_nivel.append(fondo_escalado)
                
        except pygame.error:
            # Fallback: crear un fondo sólido si no hay imágenes
            ancho_pantalla = self.pantalla.get_width()
            alto_pantalla = self.pantalla.get_height()
            fondo_solido = pygame.Surface((ancho_pantalla, alto_pantalla))
            fondo_solido.fill((0, 0, 50))  # Azul oscuro
            self.fondos_nivel.append(fondo_solido)
    
    def actualizar_fondo(self) -> None:
        """
        Actualiza el fondo actual basado en el nivel.
        """
        if self.fondos_nivel:
            indice_fondo = min(self.fondo_actual, len(self.fondos_nivel) - 1)
            self.fondo = self.fondos_nivel[indice_fondo]
    
    def subir_nivel(self) -> None:
        """
        Sube de nivel cuando se eliminan suficientes enemigos.
        """
        self.nivel_actual += 1
        self.enemigos_eliminados_nivel = 0
        self.fondo_actual = min(self.fondo_actual + 1, len(self.fondos_nivel) - 1)
        self.actualizar_fondo()
        
        # Aumentar dificultad
        self.intervalo_enemigo = max(2.0, self.intervalo_enemigo - 0.5)  # Enemigos más frecuentes

    def inicializar_juego(self) -> None:
        """
        Configura los objetos iniciales del juego.

        Crea al jugador y al enemigo en posiciones estratégicas y establece
        las relaciones entre ellos (el enemigo persigue al jugador).

        Notes
        -----
        El jugador se coloca en la parte izquierda de la pantalla y el enemigo
        en la parte superior central para un gameplay balanceado.
        """
        width = self.pantalla.get_width()
        height = self.pantalla.get_height()

        # Crear jugador (verde) en la parte izquierda de la pantalla
        self.jugador = Jugador(self.pantalla, width // 4, height // 2, (0, 255, 0))
        
        # Crear enemigo (rojo) en la parte superior central
        enemigo_inicial = Enemigo(self.pantalla, width // 2, height // 4, (255, 0, 0))
        enemigo_inicial.establecer_objetivo(self.jugador)
        self.enemigos.append(enemigo_inicial)
      
    def manejar_eventos(self) -> None:
        """
        Procesa todos los eventos de pygame en el frame actual.

        Gestiona eventos del sistema (como QUIT) y eventos de entrada del usuario
        (como clics del mouse para disparar).

        Notes
        -----
        Solo el clic izquierdo del mouse está configurado para disparar.
        El evento QUIT cambia el estado del juego para terminar el bucle principal.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    self.jugador.disparar(event.pos)

    def actualizar(self, dt: float) -> None:
        """
        Actualiza la lógica del juego en cada frame.

        Realiza las siguientes operaciones:
        1. Actualiza cooldowns globales
        2. Actualiza estado de jugador y enemigo
        3. Verifica colisiones proyectil-enemigo
        4. Verifica colisiones jugador-enemigo
        5. Gestiona respawn del enemigo
        6. Verifica condiciones de fin del juego

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

        if not self.jugando:
            return

        # 1. Actualizar cooldown de daño al jugador
        self.tiempo_desde_ultimo_dano += dt
        self.tiempo_enemigo += dt
        # Solo respawnear por tiempo si hay pocos enemigos activos
        enemigos_activos = len([e for e in self.enemigos if e.activo])
        if self.tiempo_enemigo >= self.intervalo_enemigo and enemigos_activos < 3:
           self.respawnear_enemigo()
           self.tiempo_enemigo = 0.0  # Resetear el timer
          
          
        # 2. Actualizar objetos del juego
        self.jugador.actualizar(dt)  # Actualizar jugador
        for enemigo in self.enemigos:
            if enemigo.activo:
               enemigo.actualizar(dt)



        # 3. Verificar colisiones entre proyectiles y enemigo
        self._verificar_colisiones_proyectiles()

        # 4. Verificar colisión entre jugador y enemigo
        self._verificar_colision_jugador_enemigo()

        # 5. Respawnear enemigos destruidos (controlado)
        enemigos_activos = len([e for e in self.enemigos if e.activo])
        enemigos_inactivos = len([e for e in self.enemigos if not e.activo])
        
        # Solo respawnear si hay enemigos inactivos y no hay demasiados activos
        if enemigos_inactivos > 0 and enemigos_activos < 5:
            # Solo respawnear un enemigo por frame
            self.respawnear_enemigo()

        # 6. Verificar fin del juego (puntos agotados)
        if self.puntos <= 0:
            self.jugando = False
            self.puntos = 0  # Asegurar que no sea negativo
            
        # 7. Eliminar enemigos inactivos y proyectiles inactivos
        self.enemigos = [e for e in self.enemigos if e.activo]
        self.jugador.proyectiles = [p for p in self.jugador.proyectiles if p.activo]    

    def _verificar_colisiones_proyectiles(self) -> None:
        """
        Verifica colisiones entre los proyectiles del jugador y el enemigo.

        Si un proyectil colisiona con el enemigo, le aplica daño y desactiva el proyectil.
        El jugador recibe puntos por cada golpe exitoso.

        Notes
        -----
        Se itera sobre una copia de la lista de proyectiles para evitar problemas
        al modificar la lista durante la iteración.
        """
        for proyectil in self.jugador.proyectiles[:]:  # Copia para iteración segura
            for enemigo in self.enemigos:
                if proyectil.colision(enemigo):
                   if enemigo.recibir_dano():
                        # Verificar si el enemigo fue completamente eliminado
                        if not enemigo.activo:
                            self.puntos += 1  # +1 punto por eliminar completamente al enemigo
                            self.enemigos_eliminados_nivel += 1
                            
                            # Verificar si se debe subir de nivel
                            if self.enemigos_eliminados_nivel >= self.enemigos_para_siguiente_nivel:
                                self.subir_nivel()
                        else:
                            self.puntos += 0  # No hay puntos por solo golpear
                   proyectil.activo = False

    def _verificar_colision_jugador_enemigo(self) -> None:
        """
        Verifica colisión entre el jugador y el enemigo y aplica daño si es necesario.

        El jugador recibe daño si colisiona con el enemigo y ha pasado el cooldown
        de daño establecido. Cada colisión reduce un punto.
        """
        for enemigo in self.enemigos:
           if (self.jugador.colision(enemigo) and 
              self.tiempo_desde_ultimo_dano >= self.cooldown_dano):
            
              self.puntos -= 2
              self.tiempo_desde_ultimo_dano = 0.0

    def respawnear_enemigo(self) -> None:
        """
        Reaparece el enemigo en una posición aleatoria de la pantalla.

        El nuevo enemigo mantiene la referencia al jugador como objetivo
        y reaparece con todos sus atributos reseteados (vida completa, etc.).

        Notes
        -----
        La posición aleatoria evita que el enemigo aparezca demasiado cerca
        de los bordes de la pantalla (margen de 50 píxeles).
        """
        width = self.pantalla.get_width()
        height = self.pantalla.get_height()
        
        # Generar posición aleatoria con margen de seguridad
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)

        nuevo = Enemigo(self.pantalla, x, y, (255, 0, 0), radio=random.choice([10,15,20,25,30]))
        nuevo.establecer_objetivo(self.jugador)
        self.enemigos.append(nuevo)

    def pintar(self) -> None:
        """
        Renderiza todos los elementos del juego en la pantalla.

        Según el estado del juego (activo o game over), muestra diferentes
        elementos: interfaz durante el juego, pantalla de fin cuando termina.

        Notes
        -----
        La pantalla se limpia completamente en cada frame antes de dibujar.
        El orden de renderizado es importante para la superposición de elementos.
        """
        # Limpiar pantalla con color negro
        self.pantalla.fill((0, 0, 0))

        if self.jugando:
            self._pintar_juego_activo()
        else:
            self._pintar_game_over()

        # Actualizar la pantalla completa
        pygame.display.flip()

    def _pintar_juego_activo(self) -> None:
        """
        Renderiza la interfaz del juego cuando está activo.

        Incluye:
        - Jugador y enemigos
        - Proyectiles
        - Información de puntos
        - Instrucciones de control
        """
        # ✅ Dibujar imagen de fondo
        self.pantalla.blit(self.fondo, (0, 0))
        
        # Pintar objetos del juego
        self.jugador.pintar()
        for enemigo in self.enemigos:
             if enemigo.activo:
                enemigo.pintar()

        # Mostrar información del juego
        texto_puntos = self.fuente.render(f"Puntos: {self.puntos}", True, (255, 255, 255))
        self.pantalla.blit(texto_puntos, (10, 10))
        
        # Mostrar nivel actual
        texto_nivel = self.fuente.render(f"Nivel: {self.nivel_actual}", True, (255, 255, 255))
        self.pantalla.blit(texto_nivel, (10, 50))
        
        # Mostrar progreso hacia siguiente nivel
        progreso = f"Enemigos: {self.enemigos_eliminados_nivel}/{self.enemigos_para_siguiente_nivel}"
        texto_progreso = self.fuente_pequena.render(progreso, True, (200, 200, 200))
        self.pantalla.blit(texto_progreso, (10, 90))

        # Mostrar instrucciones de control
        texto_instrucciones = self.fuente_pequena.render(
            "Mueve con mouse - Clic izquierdo para disparar", True, (200, 200, 200))
        self.pantalla.blit(texto_instrucciones, (10, 120))

    def _pintar_game_over(self) -> None:
        """
        Renderiza la pantalla de fin del juego (Game Over).

        Muestra:
        - Texto "GAME OVER" centrado
        - Puntuación final obtenida
        """
        # Texto principal de Game Over
        texto_game_over = self.fuente.render("GAME OVER", True, (255, 0, 0))
        texto_rect = texto_game_over.get_rect(
            center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2))
        self.pantalla.blit(texto_game_over, texto_rect)

        # Puntuación final
        texto_puntos_final = self.fuente.render(
            f"Puntos finales: {self.puntos}", True, (255, 255, 255))
        puntos_rect = texto_puntos_final.get_rect(
            center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2 + 40))
        self.pantalla.blit(texto_puntos_final, puntos_rect)

    def ejecutar(self) -> None:
        """
        Ejecuta el bucle principal del juego.

        Este método contiene el game loop que se ejecuta continuamente hasta
        que el juego termina. Maneja la temporización, eventos, actualización
        y renderizado en cada frame.

        Notes
        -----
        El juego se ejecuta a aproximadamente 60 FPS.
        Después del game over, espera 3 segundos antes de cerrar la aplicación.
        """
        try:
            while True:
                # Calcular delta time (tiempo transcurrido desde el último frame)
                dt = self.clock.tick(60) / 1000.0  # Convertir milisegundos a segundos

                # Procesar eventos de entrada
                self.manejar_eventos()

                # Actualizar lógica del juego si está activo
                if self.jugando:
                    self.actualizar(dt)

                # Renderizar frame actual
                self.pintar()

                # Salir después del game over
                if not self.jugando:
                    # Esperar 3 segundos en pantalla de game over antes de cerrar
                    pygame.time.wait(3000)
                    break

        except Exception as e:
            print(f"Error durante la ejecución del juego: {e}")
        finally:
            pygame.quit()

    def __repr__(self) -> str:
        """
        Representación oficial del ControlJuego para depuración.

        Returns
        -------
        str
            Cadena que representa el estado actual del juego
        """
        estado = "jugando" if self.jugando else "game over"
        jugador_activo = self.jugador.activo if self.jugador else "no inicializado"
        enemigos_activos = len([e for e in self.enemigos if e.activo]) if self.enemigos else 0
        
        return (f"ControlJuego(puntos={self.puntos}, estado={estado}, "
                f"jugador={jugador_activo}, enemigos_activos={enemigos_activos})")

    def __str__(self) -> str:
        """
        Representación legible del ControlJuego para usuarios.

        Returns
        -------
        str
            Descripción simplificada del estado del juego
        """
        return f"Juego: {self.puntos} puntos - {'Activo' if self.jugando else 'Game Over'}"

