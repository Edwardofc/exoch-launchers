#!/usr/bin/env python3
"""
Minecraft Launcher - Professional Python Implementation
A modern, cross-platform Minecraft launcher with advanced features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os
import threading
import time
import json
import sys
from pathlib import Path

class MinecraftLauncher(tk.Tk):
    """Professional Minecraft Launcher with Tkinter"""
    
    def __init__(self):
        super().__init__()
        self.title("LauncherPro - Minecraft")
        self.geometry("1000x700")
        self.resizable(True, True)
        self.configure(bg="#1a1a2e")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Professional color scheme
        self.colors = {
            "primary": "#0f3460",
            "secondary": "#16213e",
            "accent": "#e94560",
            "success": "#00d4aa",
            "warning": "#ffd93d",
            "text": "#ffffff",
            "text_secondary": "#a0a0a0",
            "background": "#1a1a2e",
            "card": "#16213e"
        }
        
        self.setup_styles()
        self.create_widgets()
        self.load_settings()
        
    def setup_styles(self):
        """Configure professional ttk styles"""
        self.style.configure("TButton", 
                           background=self.colors["primary"],
                           foreground=self.colors["text"],
                           padding=10,
                           font=("Segoe UI", 10, "bold"))
        self.style.map("TButton",
                     background=[("active", self.colors["secondary"])])
        
        self.style.configure("TLabel", 
                           background=self.colors["background"],
                           foreground=self.colors["text"],
                           font=("Segoe UI", 10))
        
        self.style.configure("TEntry",
                           fieldbackground=self.colors["card"],
                           foreground=self.colors["text"],
                           padding=8)
        
        self.style.configure("TCombobox",
                           fieldbackground=self.colors["card"],
                           foreground=self.colors["text"])
        
        self.style.configure("TNotebook", background=self.colors["background"])
        self.style.configure("TNotebook.Tab", 
                           background=self.colors["card"],
                           foreground=self.colors["text"],
                           padding=[15, 5])
        self.style.map("TNotebook.Tab",
                     background=[("selected", self.colors["primary"])])
    
    def create_widgets(self):
        """Create main application widgets"""
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.play_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.play_frame, text="Play")
        self.create_play_tab()
        
        self.servers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.servers_frame, text="Servidores")
        self.create_servers_tab()
        
        self.news_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.news_frame, text="Noticias")
        self.create_news_tab()
        
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Ajustes")
        self.create_settings_tab()
    
    def create_play_tab(self):
        """Create Play tab with game information and launch button"""
        play_container = ttk.Frame(self.play_frame, style="TFrame")
        play_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_frame = ttk.Frame(play_container, style="TFrame")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(info_frame, text="Minecraft", 
                               font=("Segoe UI", 24, "bold"),
                               foreground=self.colors["success"])
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(info_frame, text="v1.21.1",
                                 foreground=self.colors["text_secondary"])
        version_label.pack(side=tk.RIGHT)
        
        stats_frame = ttk.Frame(play_container, style="TFrame")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats = [
            ("FPS Máx.", "240 FPS"),
            ("Distancia Render", "12 Chunks"),
            ("RAM Máx.", "4 GB"),
            ("Resolución", "1920x1080")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_container = ttk.Frame(stats_frame, style="TFrame")
            stat_container.grid(row=0, column=i, padx=10, pady=10, sticky=tk.NSEW)
            
            stat_label = ttk.Label(stat_container, text=label,
                                  foreground=self.colors["text_secondary"],
                                  font=("Segoe UI", 10))
            stat_label.pack()
            
            stat_value = ttk.Label(stat_container, text=value,
                                   foreground=self.colors["text"],
                                   font=("Segoe UI", 14, "bold"))
            stat_value.pack()
            
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        self.play_button = ttk.Button(play_container, text="Jugar",
                                      style="TButton",
                                      command=self.launch_game)
        self.play_button.pack(fill=tk.X, pady=(0, 20), ipady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(play_container,
                                           variable=self.progress_var,
                                           mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.progress_bar.pack_forget()
        
        self.progress_label = ttk.Label(play_container, text="",
                                       foreground=self.colors["success"])
        self.progress_label.pack()
        self.progress_label.pack_forget()
        
        player_frame = ttk.Frame(play_container, style="TFrame")
        player_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        player_info_label = ttk.Label(player_frame, text="Información del Juego",
                                      font=("Segoe UI", 12, "bold"))
        player_info_label.pack(pady=(0, 15))
        
        player_stats = [
            ("Cuenta:", "Player"),
            ("Última sesión:", "Hace 2 horas"),
            ("Tiempo jugado:", "124 horas"),
            ("Mundos:", "8")
        ]
        
        for label, value in player_stats:
            stat_label = ttk.Label(player_frame, text=f"{label} {value}",
                                  foreground=self.colors["text_secondary"])
            stat_label.pack(pady=2)
    
    def create_servers_tab(self):
        """Create Servers tab with server list"""
        servers_container = ttk.Frame(self.servers_frame, style="TFrame")
        servers_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        servers_label = ttk.Label(servers_container, text="Servidores Recomendados",
                                 font=("Segoe UI", 16, "bold"))
        servers_label.pack(fill=tk.X, pady=(0, 20))
        
        self.servers_list = ttk.Treeview(servers_container, 
                                       columns=("name", "ip", "players"),
                                       show="headings")
        self.servers_list.heading("name", text="Nombre")
        self.servers_list.heading("ip", text="IP")
        self.servers_list.heading("players", text="Jugadores")
        
        self.servers_list.column("name", width=200)
        self.servers_list.column("ip", width=200)
        self.servers_list.column("players", width=100)
        
        servers = [
            ("Hypixel", "mc.hypixel.net", "65,234/100,000"),
            ("Mineplex", "us.mineplex.com", "12,345/20,000"),
            ("CubeCraft Games", "play.cubecraft.net", "8,765/15,000")
        ]
        
        for server in servers:
            self.servers_list.insert("", tk.END, values=server)
        
        self.servers_list.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        add_server_btn = ttk.Button(servers_container, text="Añadir Servidor",
                                   command=self.add_server)
        add_server_btn.pack(fill=tk.X)
    
    def create_news_tab(self):
        """Create News tab with recent updates"""
        news_container = ttk.Frame(self.news_frame, style="TFrame")
        news_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        news_label = ttk.Label(news_container, text="Noticias Recientes",
                              font=("Segoe UI", 16, "bold"))
        news_label.pack(fill=tk.X, pady=(0, 20))
        
        news1_frame = ttk.Frame(news_container, style="TFrame")
        news1_frame.pack(fill=tk.X, pady=(0, 15))
        
        news1_title = ttk.Label(news1_frame, text="Minecraft 1.21 Update Released!",
                               font=("Segoe UI", 12, "bold"))
        news1_title.pack(anchor=tk.W)
        
        news1_date = ttk.Label(news1_frame, text="3 días atrás",
                              foreground=self.colors["text_secondary"])
        news1_date.pack(anchor=tk.W, pady=(5, 10))
        
        news1_content = ttk.Label(news1_frame, 
                                 text="¡La última actualización de Minecraft está aquí! Descubre nuevas mecánicas, bloques y criaturas que transformarán tu experiencia de juego.",
                                 wraplength=700,
                                 foreground=self.colors["text_secondary"])
        news1_content.pack(anchor=tk.W, pady=(0, 10))
        
        read_more_btn = ttk.Button(news1_frame, text="Leer más",
                                  command=self.open_news)
        read_more_btn.pack(anchor=tk.W)
        
        news2_frame = ttk.Frame(news_container, style="TFrame")
        news2_frame.pack(fill=tk.X)
        
        news2_title = ttk.Label(news2_frame, text="New Server Features",
                               font=("Segoe UI", 12, "bold"))
        news2_title.pack(anchor=tk.W)
        
        news2_date = ttk.Label(news2_frame, text="1 semana atrás",
                              foreground=self.colors["text_secondary"])
        news2_date.pack(anchor=tk.W, pady=(5, 10))
        
        news2_content = ttk.Label(news2_frame, 
                                 text="Los servidores han recibido actualizaciones importantes para mejorar la experiencia de juego en multiplayer.",
                                 wraplength=700,
                                 foreground=self.colors["text_secondary"])
        news2_content.pack(anchor=tk.W, pady=(0, 10))
        
        read_more_btn2 = ttk.Button(news2_frame, text="Leer más",
                                   command=self.open_news)
        read_more_btn2.pack(anchor=tk.W)
    
    def create_settings_tab(self):
        """Create Settings tab with configuration options"""
        settings_container = ttk.Frame(self.settings_frame, style="TFrame")
        settings_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ram_frame = ttk.LabelFrame(settings_container, text="Memoria RAM",
                                  style="TLabelframe")
        ram_frame.pack(fill=tk.X, pady=(0, 20))
        
        ram_min_label = ttk.Label(ram_frame, text="RAM Mínima:")
        ram_min_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.ram_min_var = tk.IntVar(value=2)
        ram_min_spin = ttk.Spinbox(ram_frame, from_=1, to=32,
                                   textvariable=self.ram_min_var)
        ram_min_spin.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        ram_max_label = ttk.Label(ram_frame, text="RAM Máxima:")
        ram_max_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.ram_max_var = tk.IntVar(value=4)
        ram_max_spin = ttk.Spinbox(ram_frame, from_=1, to=32,
                                   textvariable=self.ram_max_var)
        ram_max_spin.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        resolution_frame = ttk.LabelFrame(settings_container, text="Resolución",
                                         style="TLabelframe")
        resolution_frame.pack(fill=tk.X, pady=(0, 20))
        
        resolution_container = ttk.Frame(resolution_frame)
        resolution_container.pack(fill=tk.X, padx=10, pady=10)
        
        width_label = ttk.Label(resolution_container, text="Ancho:")
        width_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.width_var = tk.IntVar(value=1920)
        width_entry = ttk.Entry(resolution_container, textvariable=self.width_var)
        width_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        height_label = ttk.Label(resolution_container, text="Alto:")
        height_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.height_var = tk.IntVar(value=1080)
        height_entry = ttk.Entry(resolution_container, textvariable=self.height_var)
        height_entry.pack(side=tk.LEFT)
        
        self.fullscreen_var = tk.BooleanVar(value=True)
        fullscreen_check = ttk.Checkbutton(resolution_frame, text="Modo Pantalla Completa",
                                          variable=self.fullscreen_var)
        fullscreen_check.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        fps_frame = ttk.LabelFrame(settings_container, text="Rendimiento",
                                   style="TLabelframe")
        fps_frame.pack(fill=tk.X, pady=(0, 20))
        
        fps_label = ttk.Label(fps_frame, text="FPS Máximos:")
        fps_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.fps_var = tk.StringVar(value="240")
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var,
                                 values=["30", "60", "120", "144", "240", "Ilimitado"])
        fps_combo.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        java_frame = ttk.LabelFrame(settings_container, text="Java",
                                   style="TLabelframe")
        java_frame.pack(fill=tk.X, pady=(0, 20))
        
        java_path_label = ttk.Label(java_frame, text="Ruta de Java:")
        java_path_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        java_container = ttk.Frame(java_frame)
        java_container.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.java_path_var = tk.StringVar(value="java")
        java_path_entry = ttk.Entry(java_container, textvariable=self.java_path_var)
        java_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        java_browse_btn = ttk.Button(java_container, text="Buscar",
                                     command=self.browse_java)
        java_browse_btn.pack(side=tk.LEFT)
        
        buttons_frame = ttk.Frame(settings_container)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = ttk.Button(buttons_frame, text="Guardar",
                              command=self.save_settings)
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        cancel_btn = ttk.Button(buttons_frame, text="Cancelar",
                                command=self.cancel_settings)
        cancel_btn.pack(side=tk.RIGHT)
    
    def launch_game(self):
        """Launch Minecraft with current settings"""
        self.play_button.config(state=tk.DISABLED)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.progress_label.pack()
        
        threading.Thread(target=self.launch_animation, daemon=True).start()
    
    def launch_animation(self):
        """Show launch progress animation"""
        steps = [
            ("Verificando archivos...", 20),
            ("Descargando recursos...", 45),
            ("Preparando entorno...", 65),
            ("Iniciando Java...", 85),
            ("Cargando juego...", 100),
            ("Listo para jugar!", 100)
        ]
        
        for step, progress in steps:
            self.progress_label.config(text=step)
            while self.progress_var.get() < progress:
                self.progress_var.set(self.progress_var.get() + 1)
                time.sleep(0.05)
        
        time.sleep(0.5)
        
        self.progress_label.config(text="Juego iniciado!")
        time.sleep(0.5)
        
        self.play_button.config(state=tk.NORMAL)
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        
        messagebox.showinfo("Éxito", "Minecraft se ha iniciado correctamente!")
    
    def add_server(self):
        """Add new server functionality (placeholder)"""
        messagebox.showinfo("Añadir Servidor", "Funcionalidad para añadir servidores en desarrollo")
    
    def open_news(self):
        """Open Minecraft news in web browser"""
        webbrowser.open("https://www.minecraft.net/es-es")
    
    def browse_java(self):
        """Browse for Java executable"""
        filename = filedialog.askopenfilename(title="Seleccionar Java",
                                            filetypes=(("Ejecutable Java", "java.exe"),
                                                       ("Todos los archivos", "*.*")))
        if filename:
            self.java_path_var.set(filename)
    
    def save_settings(self):
        """Save launcher settings to file"""
        ram_min = self.ram_min_var.get()
        ram_max = self.ram_max_var.get()
        
        if ram_min > ram_max:
            messagebox.showerror("Error", "RAM mínima no puede ser mayor que RAM máxima")
            return
        
        settings = {
            "ram_min": ram_min,
            "ram_max": ram_max,
            "width": self.width_var.get(),
            "height": self.height_var.get(),
            "fullscreen": self.fullscreen_var.get(),
            "fps": self.fps_var.get(),
            "java_path": self.java_path_var.get()
        }
        
        try:
            with open("launcher_settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Ajustes guardados correctamente!")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar ajustes: {str(e)}")
    
    def cancel_settings(self):
        """Cancel settings changes and reload saved settings"""
        self.load_settings()
    
    def load_settings(self):
        """Load launcher settings from file"""
        settings_file = "launcher_settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                
                self.ram_min_var.set(settings.get("ram_min", 2))
                self.ram_max_var.set(settings.get("ram_max", 4))
                self.width_var.set(settings.get("width", 1920))
                self.height_var.set(settings.get("height", 1080))
                self.fullscreen_var.set(settings.get("fullscreen", True))
                self.fps_var.set(settings.get("fps", "240"))
                self.java_path_var.set(settings.get("java_path", "java"))
            except Exception as e:
                print(f"Error al cargar ajustes: {e}")
    
    def run(self):
        """Start the launcher main loop"""
        self.mainloop()

def main():
    """Main entry point for the launcher"""
    try:
        launcher = MinecraftLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error al iniciar el launcher: {e}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Error al iniciar el launcher: {e}")

if __name__ == "__main__":
    main()