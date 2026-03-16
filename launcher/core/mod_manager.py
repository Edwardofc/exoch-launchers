"""
Mod Management Module
"""

import os
import zipfile
import shutil
from typing import Dict, List, Optional
import json

class ModManager:
    """Manages mod installation and management."""
    
    MOD_DIR = "mods"
    MOD_DATABASE = "mods/mod_database.json"
    
    def __init__(self):
        self.mods = self.load_mod_database()
    
    def load_mod_database(self) -> Dict[str, Dict]:
        """Load mod database from file."""
        try:
            if os.path.exists(self.MOD_DATABASE):
                with open(self.MOD_DATABASE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading mod database: {e}")
        
        return {}
    
    def save_mod_database(self):
        """Save mod database to file."""
        try:
            os.makedirs(os.path.dirname(self.MOD_DATABASE), exist_ok=True)
            with open(self.MOD_DATABASE, "w", encoding="utf-8") as f:
                json.dump(self.mods, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving mod database: {e}")
    
    def install_mod(self, mod_file: str, instance_id: str = None) -> Optional[Dict]:
        """Install a mod from file."""
        try:
            # Extract mod information
            mod_info = self.extract_mod_info(mod_file)
            
            if not mod_info:
                return None
            
            # Create mod directory if it doesn't exist
            mod_dir = self.MOD_DIR
            os.makedirs(mod_dir, exist_ok=True)
            
            # Copy mod file
            dest_path = os.path.join(mod_dir, os.path.basename(mod_file))
            shutil.copy(mod_file, dest_path)
            
            # Update mod database
            if instance_id:
                if instance_id not in self.mods:
                    self.mods[instance_id] = []
                
                if mod_info not in self.mods[instance_id]:
                    self.mods[instance_id].append(mod_info)
            else:
                if "global" not in self.mods:
                    self.mods["global"] = []
                
                if mod_info not in self.mods["global"]:
                    self.mods["global"].append(mod_info)
            
            self.save_mod_database()
            return mod_info
        
        except Exception as e:
            print(f"Error installing mod: {e}")
            return None
    
    def extract_mod_info(self, mod_file: str) -> Optional[Dict]:
        """Extract mod information from JAR file."""
        try:
            with zipfile.ZipFile(mod_file, "r") as zf:
                if "mcmod.info" in zf.namelist():
                    with zf.open("mcmod.info") as f:
                        mod_info = json.load(f)
                        return self.parse_mcmod_info(mod_info)
                
                if "fabric.mod.json" in zf.namelist():
                    with zf.open("fabric.mod.json") as f:
                        mod_info = json.load(f)
                        return self.parse_fabric_info(mod_info)
                
                if "META-INF/mods.toml" in zf.namelist():
                    with zf.open("META-INF/mods.toml") as f:
                        mod_info = f.read().decode("utf-8")
                        return self.parse_forge_info(mod_info)
            
            # Fallback: Extract from filename
            filename = os.path.basename(mod_file)
            return {
                "name": filename.split("-")[0],
                "version": filename.split("-")[1] if "-" in filename else "unknown",
                "file": filename,
                "description": "Unknown mod",
                "author": "Unknown",
                "website": "",
                "id": filename
            }
        
        except Exception as e:
            print(f"Error extracting mod info: {e}")
            return None
    
    def parse_mcmod_info(self, mod_info: List[Dict]) -> Dict:
        """Parse mcmod.info format (Legacy Forge)."""
        mod = mod_info[0]
        
        return {
            "name": mod.get("name", "Unknown Mod"),
            "version": mod.get("version", "Unknown"),
            "file": "",
            "description": mod.get("description", ""),
            "author": mod.get("authorList", ["Unknown"])[0],
            "website": mod.get("url", ""),
            "id": mod.get("modid", mod.get("name", "unknown").lower())
        }
    
    def parse_fabric_info(self, mod_info: Dict) -> Dict:
        """Parse Fabric mod.json format."""
        return {
            "name": mod_info.get("name", "Unknown Mod"),
            "version": mod_info.get("version", "Unknown"),
            "file": "",
            "description": mod_info.get("description", ""),
            "author": mod_info.get("authors", ["Unknown"])[0],
            "website": mod_info.get("contact", {}).get("homepage", ""),
            "id": mod_info.get("id", mod_info.get("name", "unknown").lower())
        }
    
    def parse_forge_info(self, mod_info: str) -> Dict:
        """Parse Forge mods.toml format."""
        # Simplified parsing for mods.toml
        name = self.extract_from_mods_toml(mod_info, "displayName")
        version = self.extract_from_mods_toml(mod_info, "version")
        description = self.extract_from_mods_toml(mod_info, "description")
        author = self.extract_from_mods_toml(mod_info, "author")
        
        return {
            "name": name or "Unknown Mod",
            "version": version or "Unknown",
            "file": "",
            "description": description or "",
            "author": author or "Unknown",
            "website": "",
            "id": (name or "unknown").lower()
        }
    
    def extract_from_mods_toml(self, content: str, key: str) -> str:
        """Extract value from mods.toml file."""
        for line in content.split("\n"):
            if key in line:
                value = line.split("=")[1].strip()
                if value.startswith('"') and value.endswith('"'):
                    return value[1:-1]
                return value
        
        return ""
    
    def get_mods(self, instance_id: str = None) -> List[Dict]:
        """Get installed mods for an instance or globally."""
        if instance_id and instance_id in self.mods:
            return self.mods[instance_id]
        elif instance_id is None and "global" in self.mods:
            return self.mods["global"]
        else:
            return []
    
    def remove_mod(self, mod_id: str, instance_id: str = None):
        """Remove a mod."""
        target = instance_id if instance_id else "global"
        
        if target in self.mods:
            self.mods[target] = [
                mod for mod in self.mods[target]
                if mod.get("id") != mod_id and mod.get("file") != mod_id
            ]
            
            self.save_mod_database()
            
            # Remove file from disk
            mod_file = next((
                mod.get("file") for mod in self.get_mods(instance_id)
                if mod.get("id") == mod_id or mod.get("file") == mod_id
            ), None)
            
            if mod_file:
                mod_path = os.path.join(self.MOD_DIR, mod_file)
                
                try:
                    if os.path.exists(mod_path):
                        os.remove(mod_path)
                except Exception as e:
                    print(f"Error removing mod file: {e}")
    
    def get_mod_by_id(self, mod_id: str, instance_id: str = None) -> Optional[Dict]:
        """Get mod by ID."""
        mods = self.get_mods(instance_id)
        
        for mod in mods:
            if mod.get("id") == mod_id or mod.get("file") == mod_id:
                return mod
        
        return None
    
    def install_modpack(self, modpack_file: str, instance_id: str):
        """Install a modpack to an instance."""
        try:
            if not zipfile.is_zipfile(modpack_file):
                raise ValueError("Modpack file must be a ZIP archive")
            
            mod_dir = os.path.join(self.INSTANCES_DIR, instance_id, "mods")
            os.makedirs(mod_dir, exist_ok=True)
            
            with zipfile.ZipFile(modpack_file, "r") as zf:
                for file_name in zf.namelist():
                    if file_name.endswith(".jar") and "mods/" in file_name:
                        zf.extract(file_name, os.path.join(self.INSTANCES_DIR, instance_id))
            
            print(f"Modpack installed to instance: {instance_id}")
            
        except Exception as e:
            print(f"Error installing modpack: {e}")
    
    def check_mod_updates(self) -> List[Dict]:
        """Check for mod updates (placeholder)."""
        return []
    
    def update_mod(self, mod_id: str, instance_id: str = None) -> bool:
        """Update a mod (placeholder)."""
        return False