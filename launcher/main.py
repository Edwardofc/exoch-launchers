"""
Minecraft Launcher Professional - Main Entry Point
Copyright (c) 2026 LauncherPro Team

Professional Minecraft launcher with Microsoft authentication, instances, mods,
skins, and modern UI.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the launcher."""
    try:
        from gui.main_window import MinecraftLauncher
        launcher = MinecraftLauncher()
        launcher.run()
    except ImportError as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error de Importación",
            f"No se pudo importar el launcher: {str(e)}\n\n"
            "Asegúrate de que todos los archivos estén en el directorio correcto."
        )
        print(f"Error de importación: {e}")
        sys.exit(1)
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            f"Error al iniciar el launcher: {str(e)}\n\n{type(e).__name__}: {e}"
        )
        print(f"Error al iniciar el launcher: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()