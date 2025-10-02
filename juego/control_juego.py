import random
import pygame
from typing import Optional

from .figura import Figura
from .jugador import Jugador
from .enemigo import Enemigo
from .proyectil import Proyectil
from .moneda import Moneda

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
        self.game_over = False  # Estado específico de game over
        self.tiempo_desde_ultimo_dano = 0.0
        self.cooldown_dano = 1.0  # 1 segundo de cooldown para recibir daño
        self.enemigos = []
        self.monedas = []  # Lista de monedas activas en el juego  
        
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
        (como clics del mouse para disparar y teclas para reiniciar).

        Notes
        -----
        - Clic izquierdo del mouse: disparar (solo si el juego está activo)
        - ESPACIO o ENTER: reiniciar juego (solo en Game Over)
        - QUIT: salir del juego
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jugando = False
            elif event.type == pygame.KEYDOWN:
                # Reiniciar juego con ESPACIO o ENTER cuando está en Game Over
                if self.game_over and event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self.reiniciar_juego()
                # Salir con ESC
                elif event.key == pygame.K_ESCAPE:
                    self.jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Clic izquierdo solo si no es Game Over
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
        if self.puntos <= 0 and not self.game_over:
            self.game_over = True
            self.jugando = False
            self.puntos = 0  # Asegurar que no sea negativo
            
        # 7. Actualizar y gestionar monedas
        self._actualizar_monedas(dt)
        
        # 8. Verificar recolección de monedas
        self._verificar_recoleccion_monedas()
        
        # 9. Eliminar enemigos inactivos, proyectiles inactivos y monedas inactivas
        self.enemigos = [e for e in self.enemigos if e.activo]
        self.jugador.proyectiles = [p for p in self.jugador.proyectiles if p.activo]
        self.monedas = [m for m in self.monedas if m.activo]    

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
                            
                            # Generar moneda de recompensa
                            self._generar_moneda_recompensa(enemigo.x, enemigo.y)
                            
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

    def _generar_moneda_recompensa(self, x: float, y: float) -> None:
        """
        Genera una moneda de recompensa en la posición donde fue eliminado el enemigo.
        
        Parameters
        ----------
        x : float
            Posición horizontal donde se eliminó el enemigo
        y : float
            Posición vertical donde se eliminó el enemigo
        """
        # Determinar el valor de la moneda basado en el nivel
        valor_base = min(3, self.nivel_actual // 2 + 1)  # Más valor en niveles altos
        
        # Crear moneda con tipo aleatorio
        moneda = Moneda(self.pantalla, x, y, tipo_mejora=None, valor_mejora=valor_base)
        self.monedas.append(moneda)

    def _actualizar_monedas(self, dt: float) -> None:
        """
        Actualiza el estado de todas las monedas activas.
        
        Parameters
        ----------
        dt : float
            Tiempo transcurrido desde la última actualización en segundos
        """
        for moneda in self.monedas:
            if moneda.activo:
                moneda.actualizar(dt)

    def _verificar_recoleccion_monedas(self) -> None:
        """
        Verifica si el jugador ha recolectado alguna moneda y aplica las mejoras.
        """
        for moneda in self.monedas[:]:  # Copia para iteración segura
            if moneda.activo and self.jugador.colision(moneda):
                # Recolectar la moneda
                mejora = moneda.recolectar()
                
                # Aplicar la mejora al jugador
                mensaje = self.jugador.aplicar_mejora(mejora['tipo'], mejora['valor'])
                
                # Añadir puntos si corresponde
                if mejora['puntos'] > 0:
                    self.puntos += mejora['puntos']
                
                # Mostrar mensaje de mejora (opcional - se puede implementar en UI)
                print(f"¡{mensaje}")
                
                # Remover la moneda de la lista
                self.monedas.remove(moneda)

    def reiniciar_juego(self) -> None:
        """
        Reinicia el juego volviendo al estado inicial.
        
        Resetea todos los valores del juego a su estado inicial y reinicia
        la partida desde el nivel 1.
        """
        # Resetear estado del juego
        self.game_over = False
        self.jugando = True
        self.puntos = 10
        
        # Resetear sistema de niveles
        self.nivel_actual = 1
        self.enemigos_eliminados_nivel = 0
        self.enemigos_para_siguiente_nivel = 3
        self.intervalo_enemigo = 5.0
        
        # Resetear fondo
        self.fondo_actual = 0
        self.actualizar_fondo()
        
        # Limpiar listas
        self.enemigos.clear()
        self.monedas.clear()
        if self.jugador:
            self.jugador.proyectiles.clear()
        
        # Resetear mejoras del jugador
        if self.jugador:
            self.jugador.mejoras = {
                'velocidad_misil': 1.0,
                'daño_misil': 1,
                'rapidez_disparo': 1.0,
                'puntos_extra': 0
            }
            self.jugador.cooldown_disparo = 0.3
        
        # Resetear timers
        self.tiempo_desde_ultimo_dano = 0.0
        self.tiempo_enemigo = 0.0
        
        # Reinicializar juego
        self.inicializar_juego()

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
        elif self.game_over:
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
        
        # Pintar monedas
        for moneda in self.monedas:
            if moneda.activo:
                moneda.pintar()

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

        # Mostrar mejoras del jugador
        mejoras = self.jugador.obtener_estado_mejoras()
        y_offset = 120
        for tipo_mejora, valor in mejoras.items():
            if valor != 1.0 and valor != 0:  # Solo mostrar mejoras aplicadas
                nombre_mejora = tipo_mejora.replace('_', ' ').title()
                if tipo_mejora == 'velocidad_misil':
                    texto_mejora = f"Velocidad Misiles: {valor:.1f}x"
                elif tipo_mejora == 'daño_misil':
                    texto_mejora = f"Daño Extra: +{valor}"
                elif tipo_mejora == 'rapidez_disparo':
                    texto_mejora = f"Cooldown: {self.jugador.cooldown_disparo:.2f}s"
                elif tipo_mejora == 'puntos_extra':
                    texto_mejora = f"Puntos Extra: +{valor}"
                else:
                    texto_mejora = f"{nombre_mejora}: {valor}"
                
                texto_mejora_render = self.fuente_pequena.render(texto_mejora, True, (100, 255, 100))
                self.pantalla.blit(texto_mejora_render, (10, y_offset))
                y_offset += 20

        # Mostrar instrucciones de control
        texto_instrucciones = self.fuente_pequena.render(
            "Mueve con mouse - Clic izquierdo para disparar - Recolecta monedas para mejoras", True, (200, 200, 200))
        self.pantalla.blit(texto_instrucciones, (10, y_offset + 10))

    def _pintar_game_over(self) -> None:
        """
        Renderiza la pantalla de fin del juego (Game Over).

        Muestra:
        - Texto "GAME OVER" centrado
        - Puntuación final obtenida
        - Instrucciones para reiniciar
        """
        # Texto principal de Game Over
        texto_game_over = self.fuente.render("GAME OVER", True, (255, 0, 0))
        texto_rect = texto_game_over.get_rect(
            center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2 - 60))
        self.pantalla.blit(texto_game_over, texto_rect)

        # Puntuación final
        texto_puntos_final = self.fuente.render(
            f"Puntos finales: {self.puntos}", True, (255, 255, 255))
        puntos_rect = texto_puntos_final.get_rect(
            center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2 - 20))
        self.pantalla.blit(texto_puntos_final, puntos_rect)
        
        # Instrucciones para reiniciar
        texto_reiniciar = self.fuente_pequena.render(
            "Presiona ESPACIO o ENTER para reiniciar", True, (200, 200, 200))
        reiniciar_rect = texto_reiniciar.get_rect(
            center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2 + 20))
        self.pantalla.blit(texto_reiniciar, reiniciar_rect)
        
        # Instrucciones para salir
        texto_salir = self.fuente_pequena.render(
            "Presiona ESC para salir", True, (150, 150, 150))
        salir_rect = texto_salir.get_rect(
            center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2 + 50))
        self.pantalla.blit(texto_salir, salir_rect)

    def ejecutar(self) -> None:
        """
        Ejecuta el bucle principal del juego.

        Este método contiene el game loop que se ejecuta continuamente hasta
        que el juego termina. Maneja la temporización, eventos, actualización
        y renderizado en cada frame.

        Notes
        -----
        El juego se ejecuta a aproximadamente 60 FPS.
        El juego no se cierra automáticamente, permite reiniciar desde Game Over.
        """
        try:
            while self.jugando or self.game_over:
                # Calcular delta time (tiempo transcurrido desde el último frame)
                dt = self.clock.tick(60) / 1000.0  # Convertir milisegundos a segundos

                # Procesar eventos de entrada
                self.manejar_eventos()

                # Actualizar lógica del juego si está activo
                if self.jugando:
                    self.actualizar(dt)

                # Renderizar frame actual
                self.pintar()

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
        if self.jugando:
            estado = "jugando"
        elif self.game_over:
            estado = "game over"
        else:
            estado = "inactivo"
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
        if self.jugando:
            estado_str = "Activo"
        elif self.game_over:
            estado_str = "Game Over"
        else:
            estado_str = "Inactivo"
        return f"Juego: {self.puntos} puntos - {estado_str}"

