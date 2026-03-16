"""
Application Exceptions and Custom Errors
"""

class LauncherError(Exception):
    """Base exception for launcher-related errors."""
    def __init__(self, message="Error en el launcher", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message

class AuthenticationError(LauncherError):
    """Error during authentication process."""
    def __init__(self, message="Error de autenticación", details=None):
        super().__init__(message, details)

class VersionNotFoundError(LauncherError):
    """Minecraft version not found or not installed."""
    def __init__(self, version="Unknown", details=None):
        super().__init__(f"Versión {version} no encontrada", details)

class DownloadError(LauncherError):
    """Error during file download."""
    def __init__(self, file="Unknown", details=None):
        super().__init__(f"Error al descargar {file}", details)

class InstanceError(LauncherError):
    """Instance-related errors."""
    def __init__(self, message="Error de instancia", details=None):
        super().__init__(message, details)

class ModError(LauncherError):
    """Mod management errors."""
    def __init__(self, message="Error de mod", details=None):
        super().__init__(message, details)

class SkinError(LauncherError):
    """Skin management errors."""
    def __init__(self, message="Error de skin", details=None):
        super().__init__(message, details)

class ConfigurationError(LauncherError):
    """Configuration errors."""
    def __init__(self, message="Error de configuración", details=None):
        super().__init__(message, details)

class GameLaunchError(LauncherError):
    """Game launch errors."""
    def __init__(self, message="Error al iniciar el juego", details=None):
        super().__init__(message, details)

# Error handler decorator
def handle_errors(func):
    """Decorator to handle exceptions in launcher functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from gui.main_window import MinecraftLauncher
            
            if hasattr(args[0], 'show_error'):
                args[0].show_error(str(e))
            else:
                print(f"Error: {e}")
            
            import traceback
            print("Stack trace:")
            print(traceback.format_exc())
            
            return None
    
    return wrapper