# Juego de Evasión y Disparo

Un juego 2D desarrollado en Python usando PyGame que demuestra principios de **Programación Orientada a Objetos** y **desarrollo de videojuegos**. El jugador controla una bola verde que debe evitar a un enemigo rojo mientras dispara proyectiles para ganar puntos.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyGame](https://img.shields.io/badge/PyGame-2.0+-green.svg)

## Características del Juego

- **Control intuitivo**: Mueve la bola verde con el mouse
- **Sistema de disparo**: Haz clic izquierdo para disparar proyectiles amarillos, en la dirección que se mueve la bola verde
- **IA enemiga**: El enemigo rojo persigue al jugador de manera inteligente (usa la ubicación)
- **Sistema de puntos**: Pierde puntos al tocar al enemigo, gana puntos al dispararle
- **Mecánicas avanzadas**: 

  - Cooldown de disparos
  - Sistema de vida del enemigo
  - Invulnerabilidad temporal tras recibir daño
  - Respawn automático del enemigo

## Arquitectura del Proyecto

El proyecto está diseñado siguiendo principios de **Programación Orientada a Objetos** y **patrones de diseño**:

### Estructura de Clases

```
├── Vector2D          # Manejo matemático de vectores 2D
├── Figura            # Clase base abstracta para entidades
│   ├── Proyectil     # Munición disparada por el jugador
│   ├── Jugador       # Entidad controlada por el usuario
│   └── Enemigo       # IA que persigue al jugador
└── ControlJuego      # Controlador principal del juego
```

- Ver el [Diagrama de Clases](refs/diagrama.md) para más detalles.

### Principios de Diseño Aplicados

- **Herencia**: Todas las entidades del juego heredan de `Figura`
- **Encapsulación**: Cada clase maneja sus propias responsabilidades
- **Polimorfismo**: Método `actualizar()` implementado específicamente en cada clase
- **Composición**: `ControlJuego` contiene y coordina todas las entidades
- **Separación de responsabilidades**: Lógica separada por funcionalidad

Este proyecto es ideal para aprender:

- **Programación Orientada a Objetos** en Python
- **Desarrollo de videojuegos** con [PyGame](https://www.pygame.org/docs/)
- **Patrones de diseño** en software
- **Matemáticas** aplicadas a juegos (vectores, colisiones)
- **Testing** con [pytest](https://docs.pytest.org/en/stable/)

## Instalación y Ejecución

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/clubdecomputacion/evadir-disparar.git
cd evadir-disparar

# Crear/Activar entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install pygame
```

### Ejecución

```bash
# Ejecutar el juego
python main.py
```

## Controles del Juego

| Acción | Control |
|--------|---------|
| Mover jugador | Mouse |
| Disparar | Click izquierdo |
| Salir | Cerrar ventana o Esc |

## Objetivos del Juego

1. **Evitar al enemigo**: No dejes que la bola roja te toque
2. **Disparar al enemigo**: Usa proyectiles para reducir su vida
3. **Ganar puntos**: Cada golpe al enemigo te da +2 puntos
4. **Sobrevivir**: Si tus puntos llegan a 0 **¡Game Over!**

## Configuración del Juego

### Parámetros Modificables

En el código puedes ajustar:

```python
# Configuración de pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Configuración del jugador
VELOCIDAD_JUGADOR = 0.1
COOLDOWN_DISPARO = 0.3  # segundos

# Configuración del enemigo
VELOCIDAD_ENEMIGO = 50  # píxeles/segundo
VIDA_ENEMIGO = 3

# Configuración de proyectiles
VELOCIDAD_PROYECTIL = 300
TIEMPO_VIDA_PROYECTIL = 2.0  # segundos
```

## Fases del Game Loop:

[Game Loop](refs/gameloop.md)

### 1. Fase de Inicialización

- Configuración inicial de PyGame
- Creación del GameManager
- Inicialización de objetos del juego

### 2. Fase de _Input_

- Manejo de eventos de PyGame
- Detección de clicks del mouse
- Control de salida del juego

### 3. Fase de _Update_

- Cálculo de delta time para movimiento consistente
- Actualización del jugador (movimiento suave hacia mouse)
- Gestión de proyectiles (movimiento, limpieza)
- IA del enemigo (persecución inteligente)
- Sistema de respawn

### 4. Fase de _Colisiones_

- Detección proyectil vs enemigo
- Sistema de daño e invulnerabilidad
- Detección jugador vs enemigo
- Actualización de puntuación

### 5. Fase de _Render_

- Limpieza de pantalla
- Renderizado condicional (juego activo vs game over)
- Actualización de display

**Características Destacadas**:

- **Delta Time**: Movimiento independiente de FPS
- **Cooldowns**: Sistemas para limitar disparos y daño continuo
- **Estados**: Manejo de entidades activas/inactivas  
- **IA Básica**: Persecución inteligente del enemigo
- **Gestión de Memoria**: Limpieza automática de proyectiles
- **Game Over**: Transición suave al final del juego

## Estructura de Archivos

```
evadir-disparar/
├── .gitignore              # Archivos a ignorar en git
├── README.md               # Documentación del proyecto
├── requirements.txt        # Dependencias del proyecto
├── main.py                 # Código principal del juego
├── juego/
│   ├── __init__.py
│   ├── control_juego.py    # Controlador principal del juego
│   ├── vector2d.py         # Manejo matemático de vectores 2D
│   ├── figura.py           # Clase base abstracta para entidades
│   ├── jugador.py          # Entidad controlada por el usuario
│   ├── proyectil.py        # Munición disparada por el jugador
│   └── enemigo.py          # IA que persigue al jugador
├── docs/                   # Documentación Técnica
└── refs/                   # Documentación adicional
    ├── diagrama.md         # Diagrama de Clases (mermaid)
    ├── diagrama.pdf
    └── gameloop.md         # Lógica de un juego
```

## Extensiones Futuras

### Funcionalidades Planeadas
- [ ] **Power-ups**: Mejoras temporales para el jugador
- [ ] **Múltiples niveles**: Dificultad progresiva
- [ ] **Diferentes tipos de enemigos**: Con comportamientos únicos
- [ ] **Sistema de puntuación**: High scores y persistencia
- [ ] **Efectos de sonido**: Audio feedback
- [ ] **Partículas**: Efectos visuales al disparar/colisionar
- [ ] **Menú principal**: Interfaz de inicio

### Mejoras Técnicas
- [ ] **Sistema de entidades-componentes**: Arquitectura más flexible
- [ ] **Pool de objetos**: Optimización de memoria para proyectiles
- [ ] **Sistema de eventos**: Comunicación desacoplada entre objetos
- [ ] **Configuración externa**: Archivos JSON para parámetros
- [ ] **Sprites**: Reemplazar formas geométricas con imágenes

