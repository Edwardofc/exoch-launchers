# Minecraft Launcher Professional

Un launcher profesional de Minecraft con autenticación de Microsoft, gestión de instancias, mods, skins y una interfaz de usuario moderna.

## Características Principales

### 🎮 **Autenticación Microsoft**
- Inicio de sesión con cuenta Microsoft
- Soporte para cuentas premium
- Gestión de tokens y sesiones
- Autenticación segura con OAuth2

### 📦 **Gestión de Instancias**
- Creación de instancias vanilla, Forge, Fabric y Quilt
- Detección automática de tipos de instancias
- Importación/exportación de modpacks
- Registro de tiempo jugado

### 🛠️ **Gestión de Mods**
- Instalación y eliminación de mods
- Detección automática de versiones compatible
- Gestión de modpacks
- Actualizaciones de mods

### 🎨 **Gestión de Skins**
- Biblioteca de skins personalizadas
- Previsualización de skins
- Aplicación dinámica de skins
- Integración con Mojang API

### ⚙️ **Configuración Avanzada**
- Personalización de tema (oscuro/claro/azul/verde)
- Ajustes de RAM y rendimiento
- Configuración de resolución
- Control de FPS y rendimiento

### 📊 **Interfaz Profesional**
- Design moderno y responsive
- Barra de progreso animada
- Información en tiempo real
- Previsualización de skins

### 🔒 **Seguridad**
- Autenticación segura OAuth2
- Verificación de archivos
- Gestión segura de datos

## Estructura del Proyecto

```
minecraft-launcher-pro/
├── launcher/                    # Código fuente principal
│   ├── main.py                 # Punto de entrada
│   ├── config/                 # Configuración
│   │   ├── launcher_config.py  # Manejador de configuración
│   │   └── launcher_config.json # Configuración predeterminada
│   ├── api/                    # Integración con APIs
│   │   ├── microsoft_auth.py   # Autenticación Microsoft
│   │   └── download_manager.py # Gestión de descargas
│   ├── core/                   # Funcionalidad core
│   │   ├── instance_manager.py # Gestión de instancias
│   │   ├── mod_manager.py      # Gestión de mods
│   │   ├── skin_manager.py     # Gestión de skins
│   │   └── exceptions.py       # Manejador de errores
│   └── gui/                    # Interfaz de usuario
│       └── main_window.py      # Ventana principal
├── instances/                  # Almacenamiento de instancias
├── mods/                       # Repositorio de mods
├── skins/                      # Biblioteca de skins
├── assets/                     # Recursos Minecraft
├── versions/                   # Versiones del juego
├── libraries/                  # Librerías Java
├── cache/                      # Caché de descargas
├── run.py                      # Script de ejecución
├── setup.py                    # Dependencias
└── STRUCTURE.md                # Guía de estructura
```

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- tkinter (biblioteca estándar de Python)
- pip (gestor de paquetes)

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar el Launcher
```bash
python run.py
```

O directamente desde el directorio `launcher`:
```bash
cd launcher
python main.py
```

## Uso del Launcher

### 1. Autenticación
1. Haga clic en "Iniciar Sesión"
2. Se abrirá el navegador web para autenticar con Microsoft
3. Complete el proceso de inicio de sesión
4. Cuando se le pida, introduzca el código de autenticación

### 2. Crear una Instancia
1. Navegue a la pestaña "Instancias"
2. Haga clic en "Crear Instancia"
3. Configure el nombre, versión y tipo de instancia
4. Haga clic en "Guardar"

### 3. Instalar Mods
1. Navegue a la pestaña "Mods"
2. Haga clic en "Instalar Mod"
3. Seleccione el archivo .jar del mod
4. El mod se instalará automáticamente

### 4. Cambiar Skin
1. Navegue a la pestaña "Skins"
2. Haga clic en "Añadir Skin"
3. Seleccione un archivo PNG de skin
4. Haga clic en "Aplicar Skin"

## Configuración

Los ajustes se guardan en el archivo `config/launcher_config.json`. Algunos ajustes clave:

```json
{
  "theme": "dark",              // Tema: dark/light/blue/green
  "min_ram": 2048,             // RAM mínima en MB
  "max_ram": 4096,             // RAM máxima en MB
  "resolution": {               // Resolución de pantalla
    "width": 1920,
    "height": 1080
  },
  "fullscreen": true,          // Pantalla completa
  "max_fps": 240,              // FPS máximos
  "render_distance": 12        // Distancia de renderizado en chunks
}
```

## Desarrollo

### Estructura de Código

#### 1. `gui/main_window.py`
Contiene la interfaz de usuario principal. Responsable de:
- Crear widgets y tablas
- Manejar eventos
- Coordinar con otros módulos

#### 2. `core/instance_manager.py`
Gestión de instancias. Funcionalidades:
- Creación/eliminación de instancias
- Detección de tipos de instancias
- Importación de modpacks

#### 3. `core/mod_manager.py`
Gestión de mods. Funcionalidades:
- Instalación/eliminación de mods
- Detección de información de mods
- Verificación de versiones

#### 4. `core/skin_manager.py`
Gestión de skins. Funcionalidades:
- Biblioteca de skins
- Previsualización de skins
- Integración con Mojang API

#### 5. `api/microsoft_auth.py`
Autenticación Microsoft. Funcionalidades:
- Flujo OAuth2
- Gestión de tokens
- Verificación de perfil

### Ejecutar Pruebas
```bash
python -m pytest tests/
```

## Contribuciones

Las contribuciones son bienvenidas! Por favor:
1. Fork el repositorio
2. Cree una rama para su característica
3. Implemente sus cambios
4. Envíe un Pull Request

## Licencia

MIT License - Ver LICENSE para más detalles

## Problemas Comunes

### Error de Importación
Verifique que el directorio `launcher` esté en el PATH de Python.

### Error de Autenticación
- Verifique su conexión a internet
- Asegúrese de que su cuenta Microsoft esté activa
- Compruebe que las credenciales sean correctas

### Error al Iniciar
- Verifique que Java esté instalado
- Compruebe que la versión de Minecraft esté descargada
- Verifique la disponibilidad de RAM

## Contacto

Si tienes preguntas o problemas:
1. Abre un issue en GitHub
2. Consulta la documentación
3. Verifica los prerequisitos de instalación

¡Disfruta de tu launcher profesional de Minecraft!
