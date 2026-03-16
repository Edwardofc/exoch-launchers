"""
Skin Management Module
"""

import os
import requests
import json
from typing import Dict, Optional
import uuid

class SkinManager:
    """Handles Minecraft skin management and preview."""
    
    SKIN_DIR = "skins"
    DEFAULT_SKIN = "http://textures.minecraft.net/texture/0000000000000000000000000000000000000000000000000000000000000000"
    
    def __init__(self):
        os.makedirs(self.SKIN_DIR, exist_ok=True)
        self.skins = self.load_skins()
    
    def load_skins(self) -> Dict[str, Dict]:
        """Load saved skins from disk."""
        try:
            skins_file = os.path.join(self.SKIN_DIR, "skins.json")
            
            if os.path.exists(skins_file):
                with open(skins_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading skins: {e}")
        
        return {}
    
    def save_skins(self):
        """Save skins to disk."""
        skins_file = os.path.join(self.SKIN_DIR, "skins.json")
        
        try:
            with open(skins_file, "w", encoding="utf-8") as f:
                json.dump(self.skins, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving skins: {e}")
    
    def add_skin(self, name: str, skin_url: str) -> str:
        """Add a new skin to the library."""
        skin_id = str(uuid.uuid4())
        
        self.skins[skin_id] = {
            "id": skin_id,
            "name": name,
            "url": skin_url,
            "timestamp": time.time(),
            "type": "custom"
        }
        
        self.save_skins()
        return skin_id
    
    def remove_skin(self, skin_id: str):
        """Remove a skin from the library."""
        if skin_id in self.skins:
            del self.skins[skin_id]
            self.save_skins()
    
    def get_skin(self, skin_id: str) -> Optional[Dict]:
        """Get skin information by ID."""
        return self.skins.get(skin_id)
    
    def get_all_skins(self) -> List[Dict]:
        """Get all saved skins."""
        return list(self.skins.values())
    
    def get_player_skin(self, username: str) -> Optional[str]:
        """Get skin from Mojang API for a specific username."""
        try:
            # Get player UUID
            uuid_response = requests.get(
                f"https://api.mojang.com/users/profiles/minecraft/{username}"
            )
            
            if uuid_response.status_code != 200:
                return None
            
            player_uuid = uuid_response.json()["id"]
            
            # Get skin URL
            profile_response = requests.get(
                f"https://sessionserver.mojang.com/session/minecraft/profile/{player_uuid}"
            )
            
            if profile_response.status_code != 200:
                return None
            
            properties = profile_response.json().get("properties", [])
            
            for prop in properties:
                if prop["name"] == "textures":
                    import base64
                    texture_data = base64.b64decode(prop["value"]).decode("utf-8")
                    texture_info = json.loads(texture_data)
                    return texture_info.get("textures", {}).get("SKIN", {}).get("url")
        
        except Exception as e:
            print(f"Error getting player skin: {e}")
        
        return None
    
    def download_skin(self, skin_url: str, save_path: str) -> bool:
        """Download a skin from URL to local file."""
        try:
            response = requests.get(skin_url, stream=True)
            response.raise_for_status()
            
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True
        
        except Exception as e:
            print(f"Error downloading skin: {e}")
            return False
    
    def get_skin_preview_url(self, skin_url: str, size: int = 100) -> str:
        """Get skin preview URL (placeholder for actual API)."""
        # In real implementation, this would use a skin preview API
        return skin_url
    
    def apply_skin(self, skin_id: str, username: str) -> bool:
        """Apply a skin to a player (placeholder)."""
        skin = self.get_skin(skin_id)
        
        if not skin:
            return False
        
        try:
            # In real implementation, this would update Mojang profile
            print(f"Applying skin {skin['name']} to {username}")
            return True
        
        except Exception as e:
            print(f"Error applying skin: {e}")
            return False
    
    def update_skin(self, skin_id: str, name: str, skin_url: str):
        """Update skin information."""
        if skin_id in self.skins:
            self.skins[skin_id].update({
                "name": name,
                "url": skin_url,
                "timestamp": time.time()
            })
            
            self.save_skins()
    
    def import_skin_from_file(self, file_path: str, name: str) -> str:
        """Import skin from local file."""
        skin_id = str(uuid.uuid4())
        skin_file = os.path.join(self.SKIN_DIR, f"{skin_id}.png")
        
        try:
            shutil.copy(file_path, skin_file)
            
            self.skins[skin_id] = {
                "id": skin_id,
                "name": name,
                "url": f"file://{skin_file}",
                "timestamp": time.time(),
                "type": "imported"
            }
            
            self.save_skins()
            return skin_id
        
        except Exception as e:
            print(f"Error importing skin: {e}")
            return ""
    
    def reset_to_default_skin(self, username: str) -> bool:
        """Reset to default Steve skin (placeholder)."""
        try:
            print(f"Resetting {username} to default skin")
            return True
        except Exception as e:
            print(f"Error resetting skin: {e}")
            return False