import sys
from tkinter import Tk, messagebox

try:
    from launcher import MinecraftLauncher
    launcher = MinecraftLauncher()
    launcher.run()
except ImportError as e:
    root = Tk()
    root.withdraw()
    messagebox.showerror("Error de Importación", f"No se pudo importar el launcher: {str(e)}\n\nAsegúrate de que el archivo launcher.py esté en el mismo directorio.")
    print(f"Error de importación: {e}")
    sys.exit(1)
except Exception as e:
    root = Tk()
    root.withdraw()
    messagebox.showerror("Error", f"Error al iniciar el launcher: {str(e)}\n\n{type(e).__name__}: {e}")
    print(f"Error al iniciar el launcher: {e}")
    sys.exit(1)