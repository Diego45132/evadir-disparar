# Game Loop

El **Game Loop** (bucle de juego) es el corazón de cualquier videojuego. En este proyecto está implementado dentro de la clase `GameManager` y representa un ciclo continuo que se ejecuta aproximadamente 60 veces por segundo, creando la ilusión de movimiento y interactividad en tiempo real.

## Qué es el Game Loop?

Un Game Loop es un patrón de diseño fundamental en videojuegos que ejecuta continuamente tres operaciones esenciales:

1. **Procesar entrada del usuario** (Input)
2. **Actualizar el estado del juego** (Update) 
3. **Renderizar la escena** (Render)

Este ciclo se repite hasta que el juego termina, creando la experiencia fluida que percibe el jugador.

## Anatomía del Game Loop

### Fase de Inicialización

Antes de entrar al bucle principal, el juego se prepara:

```python
def ejecutar(self):
    # Preparación inicial
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    jugador = Jugador(...)
    enemigo = Enemigo(...)
```

Esta fase es **crítica** porque establece el estado inicial del mundo del juego. Sin una inicialización adecuada, el juego no tendría un punto de partida coherente.

### Control de Tiempo (Delta Time)

Una característica avanzada del game loop es el uso de **delta time**:

```python
dt = self.clock.tick(60) / 1000.0  # Convierte a segundos
```

**¿Por qué es importante?**

- **Consistencia**: El juego funciona igual en computadoras rápidas y lentas
- **Suavidad**: Los movimientos son fluidos independientemente de los FPS
- **Precisión**: Los cálculos físicos son más exactos

Ejemplo: Si un proyectil debe moverse 300 píxeles por segundo, en un frame de 1/60 segundos se moverá exactamente 5 píxeles, sin importar si el juego corre a 30 o 120 FPS.

### 1. Fase de _Input_ - Qué quiere hacer el jugador?

```python
def manejar_eventos(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.jugando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.jugador.disparar(event.pos)
```

**Responsabilidades**:

- **Capturar eventos**: Clicks, teclas, cierre de ventana
- **Traducir intenciones**: Convertir input crudo en acciones del juego
- **Respuesta inmediata**: El jugador debe sentir control instantáneo

**Filosofía de diseño**: El input es sagrado. Un retraso de incluso 50ms puede hacer que el juego se sienta "pesado" o poco responsive.

### 2. Fase de _Update_ - Cómo cambia el mundo?

Esta es la fase más compleja, donde ocurre toda la **lógica del juego**:

#### Actualización del Jugador

```python
def actualizar(self, dt):
    pos_mouse = pygame.mouse.get_pos()
    objetivo = Vector2D(pos_mouse[0], pos_mouse[1])
    diferencia = objetivo - self.posicion
    self.posicion = self.posicion + diferencia * self.velocidad_movimiento
```

**Movimiento suave**: En lugar de teleportar al jugador al mouse, aplicamos **interpolación lineal** (lerp) para crear un movimiento orgánico y predecible.

#### Gestión de Proyectiles

```python
for proyectil in self.proyectiles[:]:  # Copia la lista
    proyectil.actualizar(dt)
    if not proyectil.activo:
        self.proyectiles.remove(proyectil)
```

**Nota**: Iteramos sobre una **copia** de la lista mientras modificamos la original. Esto evita errores cuando removemos elementos durante la iteración.

#### Inteligencia Artificial del Enemigo

```python
if self.objetivo and self.objetivo.activo:
    direccion = self.objetivo.posicion - self.posicion
    direccion_normalizada = direccion.normalizar()
    movimiento = direccion_normalizada * (self.velocidad * dt)
    self.posicion = self.posicion + movimiento
```

**IA Básica**: El enemigo no se teletransporta al jugador, sino que calcula la **dirección óptima** y se mueve gradualmente. Esto crea tensión porque el jugador puede predecir y evadir.

#### Sistema de Colisiones

```python
if proyectil.colision(enemigo):
    if enemigo.recibir_dano():
        self.puntos += 2
    proyectil.activo = False
```

**Detección de colisiones**: Utilizamos **geometría circular** para determinar intersecciones. Es computacionalmente eficiente y visualmente convincente.

#### Sistemas de Limites Temporales

- **Cooldown de disparo**: Evita spam de proyectiles
- **Invulnerabilidad del enemigo**: Evita daño múltiple instantáneo
- **Cooldown de daño al jugador**: Previene pérdida masiva de puntos

Estos sistemas crean **ritmo de juego** y estrategia.

### 3. Fase de _Render_ - Cómo se ve el mundo?

```python
def pintar(self):
    self.pantalla.fill((0, 0, 0))  # Lienzo en blanco
    
    if self.jugando:
        self.jugador.pintar()
        self.enemigo.pintar()
        # ... mostrar UI
    else:
        # Pantalla de Game Over
    
    pygame.display.flip()  # Mostrar todo
```

**Principios de renderizado:**

1. **Limpiar**: Borramos el frame anterior
2. **Dibujar**: Pintamos todos los elementos visibles
3. **Presentar**: Mostramos el frame completo al usuario

**Orden de dibujado**: Los elementos se dibujan en capas. El último elemento dibujado aparece "encima" de los anteriores.

## El Ciclo Infinito

```python
while self.jugando or self.puntos <= 0:
    # INPUT
    self.manejar_eventos()
    
    # UPDATE
    if self.jugando:
        self.actualizar(dt)
    
    # RENDER
    self.pintar()
    
    # Control de tiempo
    dt = self.clock.tick(60) / 1000.0
```

**¿Por qué 60 FPS?**

- **Estándar de la industria**: La mayoría de monitores funcionan a 60Hz
- **Fluidez perceptual**: El ojo humano percibe movimiento fluido a partir de ~24 FPS
- **Margen de seguridad**: 60 FPS permite caídas ocasionales sin afectar la experiencia

## Consideraciones Avanzadas

### Estado vs Eventos

- **Estado**: "El jugador está en posición (x, y)"
- **Evento**: "El jugador hizo clic"

El game loop maneja ambos elegantemente, manteniendo estado consistente mientras responde a eventos puntuales.

### Optimización de Performance

- **Lazy evaluation**: Solo calculamos lo necesario
- **Object pooling**: Reutilizamos proyectiles en lugar de crear/destruir constantemente
- **Spatial partitioning**: (No implementado, pero útil para juegos más complejos)

### Manejo de Edge Cases

- **¿Qué pasa si no hay enemigo?** → Se crea una nuevo (**respawn**)
- **¿Qué pasa si hay demasiados proyectiles?** → Los limpiamos automáticamente
- **¿Qué pasa si el jugador sale de pantalla?** → Lo mantenemos dentro de límites

## Impacto en la Experiencia del Jugador

Cada decisión en el game loop afecta directamente cómo **se siente** el juego:

- **Movimiento suave del jugador** → Sensación de control preciso
- **IA predictible del enemigo** → Tensión manejable, no frustración
- **Feedback visual inmediato** → Satisfacción al disparar
- **Sistemas de cooldown** → Ritmo estratégico, no caos

## Arquitectura y Escalabilidad

Este game loop está diseñado para **crecer**:

- **Modular**: Fácil añadir nuevos tipos de entidades
- **Extensible**: Nuevas fases (como "Physics") se integran naturalmente  
- **Mantenible**: Cada responsabilidad está claramente separada
- **Testeable**: Cada componente puede probarse independientemente

## Lecciones de Diseño

El game loop enseña principios fundamentales de programación:

1. **Separación de responsabilidades**: Input, Logic, Render
2. **Gestión del tiempo**: Delta time y scheduling
3. **Gestión de memoria**: Creación y limpieza de objetos
4. **Arquitectura orientada a eventos**: Respuesta a input del usuario
5. **Optimización prematura**: Balance entre simplicidad y performance

En conclusión, este game loop no es solo código que ejecuta un juego, sino que **orquesta** en forma coordinada los sistemas que trabajan juntos para crear una experiencia interactiva fluida, responsive y divertida. Cada frame es una pequeña secuencia de cálculos, decisiones y renderizado que, ejecutada 60 veces por segundo, cobra vida ante los ojos del jugador.

