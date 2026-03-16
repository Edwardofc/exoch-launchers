# Minecraft Launcher Python

Un launcher de Minecraft moderno y funcional desarrollado en Python con Tkinter.

## Características Principales

### 🎮 **Play**
- Botón principal para iniciar Minecraft con animación de progreso
- Información del juego en tiempo real (versión, FPS, RAM, resolución)
- Barra de progreso animada con pasos de inicialización
- Estado del jugador (última sesión, tiempo jugado, mundos)

### 🌐 **Servidores**
- Lista de servidores recomendados
- Información detallada de cada servidor (IP, jugadores)
- Funcionalidad para añadir servidores personalizados
- Diseño responsive para diferentes tamaños de ventana

### 📰 **Noticias**
- Últimas noticias sobre Minecraft
- Fechas y resúmenes de actualizaciones
- Botón para leer más noticias en la web oficial

### ⚙️ **Ajustes**
- **Memoria RAM**: Configuración de RAM mínima y máxima (1-32 GB)
- **Resolución**: Ajustes de ancho y alto de pantalla
- **Modo Pantalla Completa**: Opción para jugar en pantalla completa
- **FPS Máximos**: Selección de límites de FPS (30, 60, 120, 144, 240, Ilimitado)
- **Java**: Configuración de la ruta del ejecutable de Java
- **Persistencia**: Ajustes guardados automáticamente

## Requisitos

- Python 3.x (probado con 3.8+)
- Tkinter (incluido en Python standard library)
- Pillow (para manejo de imágenes - opcional, pero recomendado)

## Instalación

### Windows
1. Asegúrate de tener Python 3.x instalado (descarga desde [python.org](https://www.python.org/))
2. Instala Pillow (si es necesario):
   ```bash
   pip install pillow
   ```

### Linux
1. Instala Python 3.x y Tkinter:
   ```bash
   sudo apt update && sudo apt install python3 python3-pip python3-tk
   ```
2. Instala Pillow:
   ```bash
   pip3 install pillow
   ```

### macOS
1. Instala Python 3.x (usando Homebrew):
   ```bash
   brew install python3
   ```
2. Instala Pillow:
   ```bash
   pip3 install pillow
   ```

## Uso

### Modo 1: Ejecutar directamente
```bash
python3 launcher.py
```

### Modo 2: Usar el script de arranque
```bash
chmod +x run.py
./run.py
```

## Estructura del Proyecto

```
minecraft-launcher/
├── launcher.py          # Clase principal del launcher con toda la funcionalidad
├── run.py              # Script de arranque con manejo de errores
├── launcher_settings.txt # Archivo de configuración (generado automáticamente)
└── README.md           # Documentación completa
```

## Configuración

### Archivo de Ajustes

El launcher guarda los ajustes en `launcher_settings.txt` con el siguiente formato:

```txt
ram_min=2
ram_max=4
width=1920
height=1080
fullscreen=True
fps=240
java_path=java
```

### Personalización

#### Colores
Puedes modificar los colores en la sección `self.colors` de la clase `MinecraftLauncher`:
```python
self.colors = {
    "primary": "#0f3460",    # Azul oscuro
    "secondary": "#16213e",  # Azul más oscuro
    "accent": "#e94560",     # Rojo rosa
    "success": "#00d4aa",    # Verde turquesa
    "warning": "#ffd93d",    # Amarillo
    "text": "#ffffff",       # Blanco
    "text_secondary": "#a0a0a0", # Gris claro
    "background": "#1a1a2e", # Fondo principal
    "card": "#16213e"        # Color de tarjetas
}
```

#### Servidores Recomendados
Edita la lista `servers` en el método `create_servers_tab`:
```python
servers = [
    ("Nombre", "IP", "Jugadores"),
    ("Hypixel", "mc.hypixel.net", "65,234/100,000")
]
```

## Características Futuras

### Planeadas
- [ ] Autenticación con cuenta Microsoft
- [ ] Inicio real de Minecraft
- [ ] Descarga y gestión de versiones
- [ ] Manejo de mods y resource packs
- [ ] Configuración de perfiles
- [ ] Estadísticas de juego en tiempo real
- [ ] Integración con API de Minecraft
- [ ] Preview de skins
- [ ] Soporte para múltiples cuentas

### En Desarrollo
- [ ] Funcionalidad para añadir servidores personalizados
- [ ] Conexión real a servidores
- [ ] Ping y estado de servidores

## Contribuciones

Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Problemas Comunes

### Error al iniciar el launcher
- Asegúrate de tener Python 3.x instalado
- Verifica que tkinter esté disponible
- Ejecuta el script desde la línea de comandos para ver el error detallado

### El launcher no se muestra correctamente
- Verifica la resolución de tu pantalla
- Ajusta el tamaño del launcher en `self.geometry()`
- Prueba con diferentes temas de tkinter

### No se guardan los ajustes
- Asegúrate de que el script tenga permisos de escritura
- Verifica la existencia del archivo `launcher_settings.txt`
- Ejecuta el launcher como administrador si es necesario

## Licencia

MIT License - Ver LICENSE para más detalles

## Autor

Creado por [Tu Nombre] - [Enlace a tu perfil]

## Agradecimientos

- Mojang Studios por Minecraft
- Comunidad de Minecraft por su apoyo
- Desarrolladores de Python y Tkinter