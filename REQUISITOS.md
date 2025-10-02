# 🎮 Requisitos del Juego "Evadir y Disparar"

## 📋 Requisitos del Sistema

### 💻 **Sistema Operativo**
- **Windows**: 7/8/10/11 (64-bit)
- **Linux**: Ubuntu 18.04+ / Debian 10+ / CentOS 7+
- **macOS**: 10.14 (Mojave) o superior

### 🖥️ **Hardware Mínimo**
- **Procesador**: Intel Core i3 o AMD equivalente
- **Memoria RAM**: 2 GB
- **Espacio en disco**: 100 MB libres
- **Gráficos**: Tarjeta gráfica compatible con OpenGL 2.1+
- **Resolución**: Mínimo 800x600 píxeles

### 🖥️ **Hardware Recomendado**
- **Procesador**: Intel Core i5 o AMD equivalente
- **Memoria RAM**: 4 GB
- **Espacio en disco**: 200 MB libres
- **Gráficos**: Tarjeta gráfica dedicada
- **Resolución**: 1920x1080 píxeles o superior

## 🐍 Requisitos de Software

### **Python**
- **Versión**: Python 3.8 o superior
- **Recomendado**: Python 3.12+

### **Dependencias Principales**
```
pygame==2.6.1
```

### **Dependencias del Sistema (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# CentOS/RHEL
sudo yum install python3-devel python3-pip SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel
```

### **Dependencias del Sistema (Windows)**
- **Microsoft Visual C++ Redistributable** (incluido con pygame)
- **DirectX 9.0c** o superior

### **Dependencias del Sistema (macOS)**
```bash
# Con Homebrew
brew install python3 sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

## 📦 Instalación

### **Método 1: Instalación Completa**
```bash
# 1. Clonar o descargar el proyecto
git clone <url-del-repositorio>
cd evadir-disparar

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar el juego
python main.py
```

### **Método 2: Instalación Rápida**
```bash
# Instalar pygame directamente
pip install pygame==2.6.1

# Ejecutar el juego
python main.py
```

## 🎯 Controles del Juego

### **Mouse**
- **Movimiento**: Mover el mouse para controlar el avión del jugador
- **Disparo**: Clic izquierdo para disparar misiles

### **Teclado**
- **ESPACIO o ENTER**: Reiniciar juego (en pantalla Game Over)
- **ESC**: Salir del juego
- **X de ventana**: Cerrar el juego

## 🎮 Características del Juego

### **Elementos de Juego**
- ✅ **Avión Jugador**: Controlado con mouse
- ✅ **Enemigos**: Aviones enemigos que persiguen al jugador
- ✅ **Sistema de Proyectiles**: Misiles que dispara el jugador
- ✅ **Sistema de Colisiones**: Detección entre todos los elementos
- ✅ **Sistema de Vida**: Enemigos con múltiples golpes
- ✅ **Sistema de Puntos**: Puntuación basada en eliminaciones

### **Sistema de Mejoras**
- 🟢 **Monedas Verdes**: Mejoran velocidad de misiles
- 🔴 **Monedas Rojas**: Aumentan daño de misiles
- 🔵 **Monedas Azules**: Reducen tiempo entre disparos
- 🟡 **Monedas Doradas**: Otorgan puntos extra

### **Sistema de Niveles**
- ✅ **5 Niveles**: Con fondos diferentes
- ✅ **Progresión**: Dificultad aumenta por nivel
- ✅ **Enemigos por Nivel**: 3 enemigos para avanzar

## 🖼️ Recursos Gráficos

### **Archivos de Imagen Requeridos**
```
juego/static/
├── fondo_nivel1.png    # Fondo del nivel 1
├── fondo_nivel2.png    # Fondo del nivel 2
├── fondo_nivel3.png    # Fondo del nivel 3
├── fondo_nivel4.png    # Fondo del nivel 4
├── fondo_nivel5.png    # Fondo del nivel 5
└── image.png           # Fondo por defecto (fallback)
```

### **Nota sobre Recursos**
- Si las imágenes no están disponibles, el juego creará fondos sólidos como respaldo
- Las imágenes deben estar en formato PNG
- Resolución recomendada: 1920x1080 o superior

## 🐛 Solución de Problemas

### **Error: "pygame could not be resolved"**
```bash
# Reinstalar pygame
pip uninstall pygame
pip install pygame==2.6.1
```

### **Error: "No module named 'juego'"**
```bash
# Asegurarse de estar en el directorio correcto
cd evadir-disparar
python main.py
```

### **Error: "SDL could not be initialized"**
- **Linux**: Instalar dependencias SDL2
- **Windows**: Instalar Microsoft Visual C++ Redistributable
- **macOS**: Instalar Xcode Command Line Tools

### **Rendimiento Lento**
- Cerrar otras aplicaciones
- Reducir resolución de pantalla
- Verificar que no hay procesos en segundo plano

## 🔧 Configuración Avanzada

### **Modificar Resolución**
Editar en `main.py`:
```python
pantalla = pygame.display.set_mode((ANCHO, ALTO))
```

### **Modificar Velocidad del Juego**
Editar en `control_juego.py`:
```python
dt = self.clock.tick(FPS) / 1000.0  # Cambiar FPS
```

### **Modificar Dificultad**
Editar en `control_juego.py`:
```python
self.enemigos_para_siguiente_nivel = NUMERO_ENEMIGOS
self.intervalo_enemigo = TIEMPO_APARICION
```

## 📊 Rendimiento Esperado

### **FPS**
- **Objetivo**: 60 FPS
- **Mínimo**: 30 FPS
- **Máximo**: 60 FPS (limitado por diseño)

### **Uso de Memoria**
- **Inicio**: ~50 MB
- **Durante juego**: ~100 MB
- **Máximo**: ~150 MB

### **Uso de CPU**
- **Inactivo**: ~5%
- **Durante juego**: ~15-25%
- **Pico**: ~35%

## 🚀 Características Técnicas

### **Arquitectura**
- **Motor**: Pygame 2.6.1
- **Lenguaje**: Python 3.8+
- **Patrón**: MVC (Model-View-Controller)
- **Renderizado**: Software (CPU)

### **Optimizaciones**
- ✅ **Delta Time**: Tiempo variable entre frames
- ✅ **Gestión de Memoria**: Limpieza automática de objetos inactivos
- ✅ **Colisiones Optimizadas**: Detección circular eficiente
- ✅ **Renderizado Eficiente**: Solo dibuja elementos activos

## 📝 Notas de Desarrollo

### **Estructura del Código**
```
juego/
├── __init__.py          # Módulo principal
├── control_juego.py     # Controlador principal
├── figura.py           # Clase base para elementos
├── jugador.py          # Lógica del jugador
├── enemigo.py          # Lógica de enemigos
├── proyectil.py        # Lógica de misiles
├── moneda.py           # Sistema de recompensas
├── vector2d.py         # Matemáticas 2D
└── static/             # Recursos gráficos
```

### **Compatibilidad**
- ✅ **Python 3.8+**: Totalmente compatible
- ✅ **Pygame 2.6.1**: Versión específica requerida
- ✅ **Multiplataforma**: Windows, Linux, macOS
- ✅ **Arquitecturas**: x64, x86

---

## 🎯 Resumen Rápido

**Para jugar necesitas:**
1. Python 3.8+
2. pygame 2.6.1
3. 100 MB de espacio libre
4. Resolución mínima 800x600

**Para instalar:**
```bash
pip install pygame==2.6.1
python main.py
```

¡Disfruta del juego! 🚀
