"""
Launcher Configuration Manager
"""

import json
import os

class LauncherConfig:
    """Manages persistent configuration settings."""
    
    CONFIG_FILE = "config/launcher_config.json"
    
    DEFAULT_CONFIG = {
        "theme": "dark",
        "language": "es",
        "auto_login": False,
        "remember_account": True,
        "java_path": "java",
        "min_ram": 2048,
        "max_ram": 4096,
        "resolution": {
            "width": 1920,
            "height": 1080
        },
        "fullscreen": True,
        "max_fps": 240,
        "render_distance": 12,
        "show_ads": True,
        "auto_update": True,
        "download_cache": "cache"
    }
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or use defaults."""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    
                    # Merge with default config to ensure all keys are present
                    merged_config = self.DEFAULT_CONFIG.copy()
                    merged_config.update(config)
                    
                    return merged_config
        except Exception as e:
            print(f"Error loading config: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
            
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Error saving config: {e}")
    
    # Theme
    def get_theme(self):
        return self.config.get("theme", "dark")
    
    def set_theme(self, theme):
        self.config["theme"] = theme
        self.save_config()
    
    # Language
    def get_language(self):
        return self.config.get("language", "es")
    
    def set_language(self, language):
        self.config["language"] = language
        self.save_config()
    
    # Java path
    def get_java_path(self):
        return self.config.get("java_path", "java")
    
    def set_java_path(self, path):
        self.config["java_path"] = path
        self.save_config()
    
    # RAM settings
    def get_ram_settings(self):
        return {
            "min": self.config.get("min_ram", 2048),
            "max": self.config.get("max_ram", 4096)
        }
    
    def set_ram_settings(self, min_ram, max_ram):
        self.config["min_ram"] = min_ram
        self.config["max_ram"] = max_ram
        self.save_config()
    
    # Resolution
    def get_resolution(self):
        return self.config.get("resolution", {
            "width": 1920,
            "height": 1080
        })
    
    def set_resolution(self, width, height):
        self.config["resolution"] = {
            "width": width,
            "height": height
        }
        self.save_config()
    
    # Fullscreen
    def get_fullscreen(self):
        return self.config.get("fullscreen", True)
    
    def set_fullscreen(self, fullscreen):
        self.config["fullscreen"] = fullscreen
        self.save_config()
    
    # FPS limit
    def get_fps_limit(self):
        return self.config.get("max_fps", 240)
    
    def set_fps_limit(self, fps):
        self.config["max_fps"] = fps
        self.save_config()
    
    # Render distance
    def get_render_distance(self):
        return self.config.get("render_distance", 12)
    
    def set_render_distance(self, distance):
        self.config["render_distance"] = distance
        self.save_config()
    
    # Ads settings
    def get_show_ads(self):
        return self.config.get("show_ads", True)
    
    def set_show_ads(self, show):
        self.config["show_ads"] = show
        self.save_config()
    
    # Auto update
    def get_auto_update(self):
        return self.config.get("auto_update", True)
    
    def set_auto_update(self, auto_update):
        self.config["auto_update"] = auto_update
        self.save_config()
    
    # Download cache
    def get_download_cache(self):
        return self.config.get("download_cache", "cache")
    
    def set_download_cache(self, cache):
        self.config["download_cache"] = cache
        self.save_config()
    
    # Auto login
    def get_auto_login(self):
        return self.config.get("auto_login", False)
    
    def set_auto_login(self, auto_login):
        self.config["auto_login"] = auto_login
        self.save_config()
    
    # Remember account
    def get_remember_account(self):
        return self.config.get("remember_account", True)
    
    def set_remember_account(self, remember):
        self.config["remember_account"] = remember
        self.save_config()
    
    # Get all config
    def get_all_config(self):
        return self.config.copy()