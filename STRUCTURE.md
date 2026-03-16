"""
Project Structure Guide for Minecraft Launcher Professional
"""

# ===============================================
# PROJECT STRUCTURE OVERVIEW
# ===============================================
# launcher/
# ├── main.py                     # Entry point for launcher
# ├── config/                     # Configuration files
# │   ├── launcher_config.py     # Configuration manager
# │   └── launcher_config.json   # Default config (JSON)
# ├── api/                       # API integration modules
# │   ├── microsoft_auth.py      # Microsoft OAuth authentication
# │   └── download_manager.py    # Game file download management
# ├── core/                      # Core functionality modules
# │   ├── instance_manager.py    # Instance management system
# │   ├── mod_manager.py         # Mod management system
# │   ├── skin_manager.py        # Skin management system
# │   └── exceptions.py          # Custom exception classes
# ├── gui/                       # Graphical user interface
# │   └── main_window.py         # Main launcher window
# ├── instances/                 # Minecraft instances storage (generated)
# │   └── [instance_id]/         # Individual instance directories
# ├── mods/                      # Mod repository (generated)
# ├── skins/                     # Skin library (generated)
# ├── assets/                    # Minecraft assets (generated)
# ├── versions/                  # Game versions (generated)
# ├── libraries/                 # Minecraft libraries (generated)
# └── cache/                     # Download cache (generated)

# ===============================================
# INSTALLATION & DEPENDENCIES
# ===============================================
# Prerequisites:
# - Python 3.8 or higher
# - tkinter (built-in)
# - requests module for API calls
# - pillow for image processing (optional)

# Installation:
# $ pip install requests
# $ pip install pillow  # Optional, for advanced skin features

# ===============================================
# MAIN FILES - QUICK REFERENCE
# ===============================================

# 1. main.py (Entry Point)
# -------------------------
# Entry point for the entire application. Handles:
# - Error handling and exception reporting
# - Python path configuration
# - Launcher initialization

# Key features:
# - Automatic module discovery
# - Error recovery
# - CLI interface fallback

# 2. gui/main_window.py (Main Window)
# -----------------------------------
# The heart of the launcher's user interface. Contains:
# - All GUI elements and widgets
# - Event handlers for buttons and menus
# - Integration with all core features

# Key sections:
# - __init__: Initialization and module import
# - setup_styles: Theme and styling management
# - create_widgets: UI components creation
# - create_*_tab: Individual tab content
# - launch_*: Game and instance launch methods
# - Authentication methods (login, logout)
# - Settings management (save, load)

# 3. config/launcher_config.py (Configuration)
# --------------------------------------------
# Manages persistent configuration settings. Handles:
# - Configuration file loading/saving
# - Theme and appearance settings
# - Java and performance settings
# - Game window and resolution settings

# Key methods:
# - get/set: Generic configuration access
# - get_theme/set_theme: Theme management
# - get_ram_settings/set_ram_settings: RAM allocation
# - get_resolution/set_resolution: Display settings
# - get_java_path/set_java_path: Java executable path

# 4. api/microsoft_auth.py (Authentication)
# -----------------------------------------
# Handles Microsoft OAuth2 authentication flow. Features:
# - Browser-based authentication
# - Token management and refresh
# - Xbox Live integration
# - Minecraft profile verification

# Key methods:
# - authenticate(): Start OAuth2 flow
# - is_authenticated(): Check login status
# - refresh_tokens(): Token refresh
# - get_profile(): Get player profile
# - logout(): Clear authentication

# 5. core/instance_manager.py (Instance Management)
# --------------------------------------------------
# Instance system with type detection and management. Handles:
# - Instance creation and deletion
# - Vanilla, Forge, Fabric, Quilt instances
# - Modpack installation
# - Instance playtime tracking

# Key methods:
# - create_instance(): Create new instance
# - get_instances(): List all instances
# - delete_instance(): Remove instance
# - launch_instance(): Start specific instance
# - install_mod(): Install mod to instance

# 6. core/mod_manager.py (Mod Management)
# ---------------------------------------
# Mod library and installation system. Features:
# - Mod info extraction from JAR files
# - Mod database for tracking
# - Modpack installation
# - Version compatibility checks

# Key methods:
# - install_mod(): Install mod from file
# - remove_mod(): Uninstall mod
# - get_mods(): List installed mods
# - parse_mcmod_info/parse_fabric_info/parse_forge_info: Mod info extraction

# 7. core/skin_manager.py (Skin Management)
# -----------------------------------------
# Skin library and preview system. Handles:
# - Custom skin addition
# - Skin preview generation
# - Skin library management
# - Mojang API integration

# Key methods:
# - add_skin(): Add custom skin
# - get_skin_preview(): Get preview URL
# - apply_skin(): Set active skin
# - import_skin_from_file(): Import from local file

# 8. api/download_manager.py (Download Management)
# ------------------------------------------------
# Downloads and manages Minecraft assets. Handles:
# - Version manifest and game files
# - Library and asset downloads
# - Hash verification
# - Download progress tracking

# Key methods:
# - get_versions(): List available versions
# - download_version(): Download specific version
# - is_version_installed(): Check installation status

# 9. core/exceptions.py (Exception Handling)
# ------------------------------------------
# Custom exception classes and error handling. Provides:
# - Specific exception types for different errors
# - Error handler decorator
# - Centralized error reporting

# ===============================================
# DEVELOPMENT WORKFLOW
# ===============================================

# 1. Adding a New Feature
# -----------------------
# 1. Create or modify relevant module
# 2. Add UI elements in main_window.py
# 3. Add functionality in appropriate core module
# 4. Handle exceptions in exceptions.py
# 5. Update README with documentation

# 2. Modifying the UI
# --------------------
# - Main layout in create_widgets() method
# - Tab content in create_*_tab() methods
# - Styles in setup_styles()
# - Theme changes in change_theme()

# 3. Handling Events
# ------------------
# - Button clicks: Create command callbacks
# - Threading: Use daemon=True for long operations
# - Progress tracking: Update progress bar from threads

# 4. Data Persistence
# --------------------
# - Config: config/launcher_config.py
# - Instances: core/instance_manager.py (JSON files)
# - Mods: core/mod_manager.py (JSON database)
# - Skins: core/skin_manager.py (JSON library)

# ===============================================
# COMMON ISSUES & TROUBLESHOOTING
# ===============================================

# 1. Module Import Errors
# ------------------------
# - Check Python path
# - Verify module structure
# - Check dependencies

# 2. Authentication Errors
# -------------------------
# - Check internet connectivity
# - Verify Microsoft Account permissions
# - Check client_id configuration

# 3. Download Errors
# -------------------
# - Check internet connection
# - Verify storage permissions
# - Clear cache directory

# 4. Game Launch Errors
# ----------------------
# - Verify Java installation
# - Check RAM allocation
# - Verify game files

# ===============================================
# EXTENDING THE LAUNCHER
# ===============================================

# Adding a New Tab:
# 1. Create create_tabname_tab() method
# 2. Add tab to create_widgets()
# 3. Implement tab content
# 4. Add event handlers

# Adding a New Feature Module:
# 1. Create new file in appropriate directory
# 2. Implement core functionality
# 3. Add integration in main_window.py
# 4. Create UI elements and callbacks

# Adding Themes:
# 1. Add theme colors to setup_styles()
# 2. Add radio button to settings tab
# 3. Implement refresh_ui() method

# ===============================================
# KEY FILES FOR CUSTOMIZATION
# ===============================================
# - config/launcher_config.py: Configuration defaults
# - gui/main_window.py: UI and styling
# - core/instance_manager.py: Instance behavior
# - core/mod_manager.py: Mod handling
# - api/microsoft_auth.py: Authentication
# - config/launcher_config.json: Default config file