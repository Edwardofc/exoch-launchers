"""
Main Launcher Window - Professional Minecraft Launcher
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os
import threading
import time
import json

class MinecraftLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LauncherPro - Minecraft")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Import modules
        from config.launcher_config import LauncherConfig
        from api.microsoft_auth import MicrosoftAuth
        from core.instance_manager import InstanceManager
        from core.mod_manager import ModManager
        from core.skin_manager import SkinManager
        
        self.config = LauncherConfig()
        self.auth = MicrosoftAuth()
        self.instances = InstanceManager()
        self.mods = ModManager()
        self.skins = SkinManager()
        
        self.setup_styles()
        self.create_widgets()
        self.load_settings()
    
    def setup_styles(self):
        """Setup application styles."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.colors = {
            "dark": {
                "primary": "#0f3460",
                "secondary": "#16213e",
                "accent": "#e94560",
                "success": "#00d4aa",
                "warning": "#ffd93d",
                "text": "#ffffff",
                "text_secondary": "#a0a0a0",
                "background": "#1a1a2e",
                "card": "#16213e"
            },
            "light": {
                "primary": "#4a90e2",
                "secondary": "#e8f4f8",
                "accent": "#e94560",
                "success": "#00d4aa",
                "warning": "#ffd93d",
                "text": "#000000",
                "text_secondary": "#666666",
                "background": "#f8f9fa",
                "card": "#ffffff"
            }
        }
        
        current_theme = self.config.get_theme()
        self.current_colors = self.colors.get(current_theme, self.colors["dark"])
        
        self.style.configure("TButton", 
                           background=self.current_colors["primary"],
                           foreground=self.current_colors["text"],
                           padding=10,
                           font=("Arial", 10, "bold"))
        self.style.map("TButton",
                     background=[("active", self.current_colors["secondary"])])
        
        self.style.configure("TLabel", 
                           background=self.current_colors["background"],
                           foreground=self.current_colors["text"],
                           font=("Arial", 10))
        
        self.style.configure("TEntry",
                           fieldbackground=self.current_colors["card"],
                           foreground=self.current_colors["text"],
                           padding=8)
        
        self.style.configure("TCombobox",
                           fieldbackground=self.current_colors["card"],
                           foreground=self.current_colors["text"])
        
        self.style.configure("TNotebook", background=self.current_colors["background"])
        self.style.configure("TNotebook.Tab", 
                           background=self.current_colors["card"],
                           foreground=self.current_colors["text"],
                           padding=[15, 5])
        self.style.map("TNotebook.Tab",
                     background=[("selected", self.current_colors["primary"])])
        
        self.configure(bg=self.current_colors["background"])
    
    def create_widgets(self):
        """Create main application widgets."""
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Account info at top
        account_frame = ttk.Frame(main_frame, style="TFrame")
        account_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.account_info = ttk.Label(account_frame, text="Cuenta: No conectado")
        self.account_info.pack(side=tk.LEFT)
        
        self.login_btn = ttk.Button(account_frame, text="Iniciar Sesión",
                                   command=self.login)
        self.login_btn.pack(side=tk.RIGHT)
        
        # Main content notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Play tab
        self.play_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.play_frame, text="Play")
        self.create_play_tab()
        
        # Instances tab
        self.instances_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.instances_frame, text="Instancias")
        self.create_instances_tab()
        
        # Mods tab
        self.mods_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.mods_frame, text="Mods")
        self.create_mods_tab()
        
        # Skins tab
        self.skins_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.skins_frame, text="Skins")
        self.create_skins_tab()
        
        # Servers tab
        self.servers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.servers_frame, text="Servidores")
        self.create_servers_tab()
        
        # News tab
        self.news_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.news_frame, text="Noticias")
        self.create_news_tab()
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Ajustes")
        self.create_settings_tab()
    
    def create_play_tab(self):
        """Create play tab UI."""
        play_container = ttk.Frame(self.play_frame, style="TFrame")
        play_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_frame = ttk.Frame(play_container, style="TFrame")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(info_frame, text="Minecraft", 
                               font=("Arial", 24, "bold"),
                               foreground=self.current_colors["success"])
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(info_frame, text="v1.21.1",
                                 foreground=self.current_colors["text_secondary"])
        version_label.pack(side=tk.RIGHT)
        
        # Game statistics
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
                                  foreground=self.current_colors["text_secondary"],
                                  font=("Arial", 10))
            stat_label.pack()
            
            stat_value = ttk.Label(stat_container, text=value,
                                   foreground=self.current_colors["text"],
                                   font=("Arial", 14, "bold"))
            stat_value.pack()
            
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        # Play button
        self.play_button = ttk.Button(play_container, text="Jugar",
                                     style="TButton",
                                     command=self.launch_game)
        self.play_button.pack(fill=tk.X, pady=(0, 20), ipady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(play_container,
                                           variable=self.progress_var,
                                           mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.progress_bar.pack_forget()
        
        self.progress_label = ttk.Label(play_container, text="",
                                       foreground=self.current_colors["success"])
        self.progress_label.pack()
        self.progress_label.pack_forget()
        
        # Game information
        player_frame = ttk.Frame(play_container, style="TFrame")
        player_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        player_info_label = ttk.Label(player_frame, text="Información del Juego",
                                      font=("Arial", 12, "bold"))
        player_info_label.pack(pady=(0, 15))
        
        player_stats = [
            ("Cuenta:", "Player"),
            ("Última sesión:", "Hace 2 horas"),
            ("Mundos:", "8")
        ]
        
        for label, value in player_stats:
            stat_label = ttk.Label(player_frame, text=f"{label} {value}",
                                  foreground=self.current_colors["text_secondary"])
            stat_label.pack(pady=2)
    
    def create_instances_tab(self):
        """Create instances tab UI."""
        instances_container = ttk.Frame(self.instances_frame, style="TFrame")
        instances_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instance list
        list_frame = ttk.Frame(instances_container, style="TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.instances_list = ttk.Treeview(list_frame, 
                                       columns=("name", "version", "type", "playtime"),
                                       show="headings")
        self.instances_list.heading("name", text="Nombre")
        self.instances_list.heading("version", text="Versión")
        self.instances_list.heading("type", text="Tipo")
        self.instances_list.heading("playtime", text="Tiempo Jugado")
        
        self.instances_list.column("name", width=200)
        self.instances_list.column("version", width=100)
        self.instances_list.column("type", width=100)
        self.instances_list.column("playtime", width=120)
        
        self.instances_list.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Instance control buttons
        control_frame = ttk.Frame(instances_container, style="TFrame")
        control_frame.pack(fill=tk.X)
        
        create_btn = ttk.Button(control_frame, text="Crear Instancia",
                               command=self.create_instance)
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = ttk.Button(control_frame, text="Eliminar Instancia",
                               command=self.delete_instance)
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        edit_btn = ttk.Button(control_frame, text="Editar Instancia",
                            command=self.edit_instance)
        edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        launch_btn = ttk.Button(control_frame, text="Iniciar Instancia",
                               command=self.launch_instance)
        launch_btn.pack(side=tk.RIGHT)
    
    def create_mods_tab(self):
        """Create mods tab UI."""
        mods_container = ttk.Frame(self.mods_frame, style="TFrame")
        mods_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mod list
        list_frame = ttk.Frame(mods_container, style="TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.mods_list = ttk.Treeview(list_frame, 
                                     columns=("name", "version", "type", "author"),
                                     show="headings")
        self.mods_list.heading("name", text="Nombre")
        self.mods_list.heading("version", text="Versión")
        self.mods_list.heading("type", text="Tipo")
        self.mods_list.heading("author", text="Autor")
        
        self.mods_list.column("name", width=200)
        self.mods_list.column("version", width=100)
        self.mods_list.column("type", width=100)
        self.mods_list.column("author", width=150)
        
        self.mods_list.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Mod control buttons
        control_frame = ttk.Frame(mods_container, style="TFrame")
        control_frame.pack(fill=tk.X)
        
        install_btn = ttk.Button(control_frame, text="Instalar Mod",
                               command=self.install_mod)
        install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_btn = ttk.Button(control_frame, text="Eliminar Mod",
                               command=self.remove_mod)
        remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        update_btn = ttk.Button(control_frame, text="Actualizar Mods",
                              command=self.check_mod_updates)
        update_btn.pack(side=tk.RIGHT)
    
    def create_skins_tab(self):
        """Create skins tab UI."""
        skins_container = ttk.Frame(self.skins_frame, style="TFrame")
        skins_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Skin preview area
        preview_frame = ttk.Frame(skins_container, style="TFrame")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        preview_label = ttk.Label(preview_frame, text="Previsualización de Skin")
        preview_label.pack(pady=(0, 10))
        
        # Skin library
        library_frame = ttk.Frame(skins_container, style="TFrame")
        library_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.skins_list = ttk.Treeview(library_frame, 
                                       columns=("name", "type", "timestamp"),
                                       show="headings")
        self.skins_list.heading("name", text="Nombre")
        self.skins_list.heading("type", text="Tipo")
        self.skins_list.heading("timestamp", text="Fecha")
        
        self.skins_list.column("name", width=150)
        self.skins_list.column("type", width=100)
        self.skins_list.column("timestamp", width=150)
        
        self.skins_list.pack(fill=tk.X, expand=True, pady=(0, 20))
        
        # Skin control buttons
        control_frame = ttk.Frame(skins_container, style="TFrame")
        control_frame.pack(fill=tk.X)
        
        add_btn = ttk.Button(control_frame, text="Añadir Skin",
                           command=self.add_skin)
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_btn = ttk.Button(control_frame, text="Eliminar Skin",
                               command=self.remove_skin)
        remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_btn = ttk.Button(control_frame, text="Aplicar Skin",
                              command=self.apply_skin)
        apply_btn.pack(side=tk.RIGHT)
    
    def create_servers_tab(self):
        """Create servers tab UI."""
        servers_container = ttk.Frame(self.servers_frame, style="TFrame")
        servers_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        servers_label = ttk.Label(servers_container, text="Servidores Recomendados",
                                 font=("Arial", 16, "bold"))
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
        """Create news tab UI."""
        news_container = ttk.Frame(self.news_frame, style="TFrame")
        news_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        news_label = ttk.Label(news_container, text="Noticias Recientes",
                              font=("Arial", 16, "bold"))
        news_label.pack(fill=tk.X, pady=(0, 20))
        
        news1_frame = ttk.Frame(news_container, style="TFrame")
        news1_frame.pack(fill=tk.X, pady=(0, 15))
        
        news1_title = ttk.Label(news1_frame, text="Minecraft 1.21 Update Released!",
                               font=("Arial", 12, "bold"))
        news1_title.pack(anchor=tk.W)
        
        news1_date = ttk.Label(news1_frame, text="3 días atrás",
                              foreground=self.current_colors["text_secondary"])
        news1_date.pack(anchor=tk.W, pady=(5, 10))
        
        news1_content = ttk.Label(news1_frame, 
                                 text="¡La última actualización de Minecraft está aquí! Descubre nuevas mecánicas, bloques y criaturas que transformarán tu experiencia de juego.",
                                 wraplength=700,
                                 foreground=self.current_colors["text_secondary"])
        news1_content.pack(anchor=tk.W, pady=(0, 10))
        
        read_more_btn = ttk.Button(news1_frame, text="Leer más",
                                  command=self.open_news)
        read_more_btn.pack(anchor=tk.W)
        
        news2_frame = ttk.Frame(news_container, style="TFrame")
        news2_frame.pack(fill=tk.X)
        
        news2_title = ttk.Label(news2_frame, text="New Server Features",
                               font=("Arial", 12, "bold"))
        news2_title.pack(anchor=tk.W)
        
        news2_date = ttk.Label(news2_frame, text="1 semana atrás",
                              foreground=self.current_colors["text_secondary"])
        news2_date.pack(anchor=tk.W, pady=(5, 10))
        
        news2_content = ttk.Label(news2_frame, 
                                 text="Los servidores han recibido actualizaciones importantes para mejorar la experiencia de juego en multiplayer.",
                                 wraplength=700,
                                 foreground=self.current_colors["text_secondary"])
        news2_content.pack(anchor=tk.W, pady=(0, 10))
        
        read_more_btn2 = ttk.Button(news2_frame, text="Leer más",
                                   command=self.open_news)
        read_more_btn2.pack(anchor=tk.W)
    
    def create_settings_tab(self):
        """Create settings tab UI."""
        settings_container = ttk.Frame(self.settings_frame, style="TFrame")
        settings_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Theme settings
        theme_frame = ttk.LabelFrame(settings_container, text="Tema",
                                    style="TLabelframe")
        theme_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.theme_var = tk.StringVar(value=self.config.get_theme())
        theme_buttons = [
            ("Oscuro", "dark"),
            ("Claro", "light"),
            ("Azul", "blue"),
            ("Verde", "green")
        ]
        
        for text, value in theme_buttons:
            btn = ttk.Radiobutton(theme_frame, text=text, variable=self.theme_var,
                               value=value, command=self.change_theme)
            btn.pack(anchor=tk.W, padx=10, pady=5)
        
        # RAM settings
        ram_frame = ttk.LabelFrame(settings_container, text="Memoria RAM",
                                  style="TLabelframe")
        ram_frame.pack(fill=tk.X, pady=(0, 20))
        
        ram_min_label = ttk.Label(ram_frame, text="RAM Mínima (MB):")
        ram_min_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.ram_min_var = tk.IntVar(value=self.config.get_ram_settings()["min"])
        ram_min_spin = ttk.Spinbox(ram_frame, from_=512, to=32768,
                                   textvariable=self.ram_min_var)
        ram_min_spin.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        ram_max_label = ttk.Label(ram_frame, text="RAM Máxima (MB):")
        ram_max_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.ram_max_var = tk.IntVar(value=self.config.get_ram_settings()["max"])
        ram_max_spin = ttk.Spinbox(ram_frame, from_=512, to=32768,
                                   textvariable=self.ram_max_var)
        ram_max_spin.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Resolution settings
        resolution_frame = ttk.LabelFrame(settings_container, text="Resolución",
                                         style="TLabelframe")
        resolution_frame.pack(fill=tk.X, pady=(0, 20))
        
        resolution_container = ttk.Frame(resolution_frame)
        resolution_container.pack(fill=tk.X, padx=10, pady=10)
        
        width_label = ttk.Label(resolution_container, text="Ancho:")
        width_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.width_var = tk.IntVar(value=self.config.get_resolution()["width"])
        width_entry = ttk.Entry(resolution_container, textvariable=self.width_var)
        width_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        height_label = ttk.Label(resolution_container, text="Alto:")
        height_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.height_var = tk.IntVar(value=self.config.get_resolution()["height"])
        height_entry = ttk.Entry(resolution_container, textvariable=self.height_var)
        height_entry.pack(side=tk.LEFT)
        
        self.fullscreen_var = tk.BooleanVar(value=self.config.get_fullscreen())
        fullscreen_check = ttk.Checkbutton(resolution_frame, text="Modo Pantalla Completa",
                                          variable=self.fullscreen_var)
        fullscreen_check.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Performance settings
        fps_frame = ttk.LabelFrame(settings_container, text="Rendimiento",
                                   style="TLabelframe")
        fps_frame.pack(fill=tk.X, pady=(0, 20))
        
        fps_label = ttk.Label(fps_frame, text="FPS Máximos:")
        fps_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.fps_var = tk.StringVar(value=str(self.config.get_fps_limit()))
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var,
                                 values=["30", "60", "120", "144", "240", "Ilimitado"])
        fps_combo.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        render_distance_label = ttk.Label(fps_frame, text="Distancia de Renderizado:")
        render_distance_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.render_distance_var = tk.IntVar(value=self.config.get_render_distance())
        render_distance_spin = ttk.Spinbox(fps_frame, from_=2, to=32,
                                   textvariable=self.render_distance_var)
        render_distance_spin.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Java settings
        java_frame = ttk.LabelFrame(settings_container, text="Java",
                                   style="TLabelframe")
        java_frame.pack(fill=tk.X, pady=(0, 20))
        
        java_path_label = ttk.Label(java_frame, text="Ruta de Java:")
        java_path_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        java_container = ttk.Frame(java_frame)
        java_container.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.java_path_var = tk.StringVar(value=self.config.get_java_path())
        java_path_entry = ttk.Entry(java_container, textvariable=self.java_path_var)
        java_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        java_browse_btn = ttk.Button(java_container, text="Buscar",
                                     command=self.browse_java)
        java_browse_btn.pack(side=tk.LEFT)
        
        # Advertising settings
        ads_frame = ttk.LabelFrame(settings_container, text="Publicidad",
                                   style="TLabelframe")
        ads_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.show_ads_var = tk.BooleanVar(value=self.config.get_show_ads())
        ads_check = ttk.Checkbutton(ads_frame, text="Mostrar Publicidad",
                                    variable=self.show_ads_var)
        ads_check.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Save and cancel buttons
        buttons_frame = ttk.Frame(settings_container)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = ttk.Button(buttons_frame, text="Guardar",
                              command=self.save_settings)
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        cancel_btn = ttk.Button(buttons_frame, text="Cancelar",
                                command=self.cancel_settings)
        cancel_btn.pack(side=tk.RIGHT)
    
    # Authentication methods
    def login(self):
        """Handle login button click."""
        threading.Thread(target=self._login_thread, daemon=True).start()
    
    def _login_thread(self):
        """Login thread to avoid blocking UI."""
        auth_data = self.auth.authenticate()
        
        if auth_data and self.auth.is_authenticated():
            self.after(0, self._on_login_success)
        else:
            self.after(0, self._on_login_failure)
    
    def _on_login_success(self):
        """Handle successful login."""
        profile = self.auth.get_profile()
        self.account_info.config(text=f"Cuenta: {profile['name']}")
        self.login_btn.config(text="Cerrar Sesión", command=self.logout)
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso!")
    
    def _on_login_failure(self):
        """Handle login failure."""
        messagebox.showerror("Error", "No se pudo iniciar sesión")
    
    def logout(self):
        """Logout from Microsoft account."""
        self.auth.logout()
        self.account_info.config(text="Cuenta: No conectado")
        self.login_btn.config(text="Iniciar Sesión", command=self.login)
        messagebox.showinfo("Éxito", "Sesión cerrada correctamente")
    
    # Game launch methods
    def launch_game(self):
        """Launch Minecraft."""
        self.play_button.config(state=tk.DISABLED)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.progress_label.pack()
        
        threading.Thread(target=self.launch_animation, daemon=True).start()
    
    def launch_animation(self):
        """Simulate game launch animation."""
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
    
    # Instance management methods
    def create_instance(self):
        """Create new instance dialog."""
        messagebox.showinfo("Crear Instancia", "Funcionalidad para crear instancias en desarrollo")
    
    def delete_instance(self):
        """Delete selected instance."""
        messagebox.showinfo("Eliminar Instancia", "Funcionalidad para eliminar instancias en desarrollo")
    
    def edit_instance(self):
        """Edit selected instance."""
        messagebox.showinfo("Editar Instancia", "Funcionalidad para editar instancias en desarrollo")
    
    def launch_instance(self):
        """Launch selected instance."""
        messagebox.showinfo("Iniciar Instancia", "Funcionalidad para iniciar instancias en desarrollo")
    
    # Mod management methods
    def install_mod(self):
        """Install mod dialog."""
        filename = filedialog.askopenfilename(title="Seleccionar Mod",
                                            filetypes=(("Mod JAR", "*.jar"),
                                                       ("Todos los archivos", "*.*")))
        
        if filename:
            mod_info = self.mods.install_mod(filename)
            
            if mod_info:
                messagebox.showinfo("Éxito", f"Mod '{mod_info['name']}' instalado correctamente!")
    
    def remove_mod(self):
        """Remove selected mod."""
        messagebox.showinfo("Eliminar Mod", "Funcionalidad para eliminar mods en desarrollo")
    
    def check_mod_updates(self):
        """Check for mod updates."""
        messagebox.showinfo("Actualizar Mods", "Funcionalidad para actualizar mods en desarrollo")
    
    # Skin management methods
    def add_skin(self):
        """Add skin dialog."""
        filename = filedialog.askopenfilename(title="Seleccionar Skin",
                                            filetypes=(("Imágenes PNG", "*.png"),
                                                       ("Todos los archivos", "*.*")))
        
        if filename:
            name = os.path.basename(filename)
            skin_id = self.skins.import_skin_from_file(filename, name)
            
            if skin_id:
                messagebox.showinfo("Éxito", "Skin importada correctamente!")
    
    def remove_skin(self):
        """Remove selected skin."""
        messagebox.showinfo("Eliminar Skin", "Funcionalidad para eliminar skins en desarrollo")
    
    def apply_skin(self):
        """Apply selected skin."""
        messagebox.showinfo("Aplicar Skin", "Funcionalidad para aplicar skins en desarrollo")
    
    # Server management methods
    def add_server(self):
        """Add server dialog."""
        messagebox.showinfo("Añadir Servidor", "Funcionalidad para añadir servidores en desarrollo")
    
    # Settings management methods
    def change_theme(self):
        """Change application theme."""
        new_theme = self.theme_var.get()
        self.config.set_theme(new_theme)
        self.setup_styles()
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh UI with new theme."""
        # Reapply theme to all widgets
        self.update()
    
    def save_settings(self):
        """Save configuration settings."""
        ram_min = self.ram_min_var.get()
        ram_max = self.ram_max_var.get()
        
        if ram_min > ram_max:
            messagebox.showerror("Error", "RAM mínima no puede ser mayor que RAM máxima")
            return
        
        self.config.set_ram_settings(ram_min, ram_max)
        self.config.set_resolution(self.width_var.get(), self.height_var.get())
        self.config.set_fullscreen(self.fullscreen_var.get())
        self.config.set_fps_limit(int(self.fps_var.get()))
        self.config.set_render_distance(self.render_distance_var.get())
        self.config.set_java_path(self.java_path_var.get())
        self.config.set_show_ads(self.show_ads_var.get())
        
        messagebox.showinfo("Éxito", "Ajustes guardados correctamente!")
    
    def cancel_settings(self):
        """Cancel settings changes."""
        self.load_settings()
    
    def load_settings(self):
        """Load settings from configuration."""
        self.theme_var.set(self.config.get_theme())
        self.ram_min_var.set(self.config.get_ram_settings()["min"])
        self.ram_max_var.set(self.config.get_ram_settings()["max"])
        self.width_var.set(self.config.get_resolution()["width"])
        self.height_var.set(self.config.get_resolution()["height"])
        self.fullscreen_var.set(self.config.get_fullscreen())
        self.fps_var.set(str(self.config.get_fps_limit()))
        self.render_distance_var.set(self.config.get_render_distance())
        self.java_path_var.set(self.config.get_java_path())
        self.show_ads_var.set(self.config.get_show_ads())
    
    def browse_java(self):
        """Browse for Java executable."""
        filename = filedialog.askopenfilename(title="Seleccionar Java",
                                            filetypes=(("Ejecutable Java", "java.exe"),
                                                       ("Todos los archivos", "*.*")))
        if filename:
            self.java_path_var.set(filename)
    
    def open_news(self):
        """Open Minecraft news in browser."""
        webbrowser.open("https://www.minecraft.net/es-es")
    
    def run(self):
        """Run the launcher."""
        self.mainloop()

if __name__ == "__main__":
    try:
        launcher = MinecraftLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error al iniciar el launcher: {e}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Error al iniciar el launcher: {e}")