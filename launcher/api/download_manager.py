"""
Launcher API - Game Download Manager
"""

import requests
import os
import zipfile
import shutil
from typing import Dict, List, Optional
import threading
from queue import Queue

class DownloadManager:
    """Manages Minecraft game and asset downloads."""
    
    DOWNLOAD_CACHE = "cache"
    VERSIONS_DIR = "versions"
    LIBRARIES_DIR = "libraries"
    ASSETS_DIR = "assets"
    
    # Mojang API endpoints
    VERSIONS_MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
    VERSION_INFO_BASE = "https://piston-meta.mojang.com"
    
    def __init__(self):
        self.download_queue = Queue()
        self.current_download = None
        self.progress_callback = None
    
    def get_versions(self) -> List[Dict]:
        """Get list of available Minecraft versions."""
        try:
            response = requests.get(self.VERSIONS_MANIFEST)
            response.raise_for_status()
            manifest = response.json()
            
            return manifest.get("versions", [])
        
        except Exception as e:
            print(f"Error getting versions: {e}")
            return []
    
    def get_version_info(self, version_id: str) -> Optional[Dict]:
        """Get detailed version information."""
        try:
            response = requests.get(self.VERSIONS_MANIFEST)
            response.raise_for_status()
            manifest = response.json()
            
            version_info = next(
                (v for v in manifest.get("versions", []) if v["id"] == version_id),
                None
            )
            
            if version_info:
                version_response = requests.get(version_info["url"])
                version_response.raise_for_status()
                return version_response.json()
        
        except Exception as e:
            print(f"Error getting version info: {e}")
        
        return None
    
    def download_version(self, version_id: str, callback=None) -> bool:
        """Download a specific Minecraft version."""
        version_info = self.get_version_info(version_id)
        
        if not version_info:
            return False
        
        # Create directories
        os.makedirs(self.VERSIONS_DIR, exist_ok=True)
        os.makedirs(self.LIBRARIES_DIR, exist_ok=True)
        os.makedirs(self.ASSETS_DIR, exist_ok=True)
        
        # Download client
        if not self.download_client(version_info, callback):
            return False
        
        # Download libraries
        if not self.download_libraries(version_info, callback):
            return False
        
        # Download assets
        if not self.download_assets(version_info, callback):
            return False
        
        # Save version info
        self.save_version_info(version_info)
        
        return True
    
    def download_client(self, version_info: Dict, callback) -> bool:
        """Download Minecraft client JAR file."""
        client_url = version_info["downloads"]["client"]["url"]
        client_hash = version_info["downloads"]["client"]["sha1"]
        client_path = os.path.join(self.VERSIONS_DIR, version_info["id"], f"{version_info['id']}.jar")
        
        os.makedirs(os.path.dirname(client_path), exist_ok=True)
        
        if os.path.exists(client_path) and self.verify_file(client_path, client_hash):
            return True
        
        try:
            self.download_file(client_url, client_path, callback)
            
            if not self.verify_file(client_path, client_hash):
                os.remove(client_path)
                return False
            
            return True
        
        except Exception as e:
            print(f"Error downloading client: {e}")
            return False
    
    def download_libraries(self, version_info: Dict, callback) -> bool:
        """Download required libraries."""
        libraries = version_info.get("libraries", [])
        
        for lib in libraries:
            try:
                if not self.download_library(lib, callback):
                    return False
            except Exception as e:
                print(f"Error downloading library: {e}")
                return False
        
        return True
    
    def download_library(self, lib: Dict, callback) -> bool:
        """Download a single library."""
        lib_name = lib["name"]
        lib_parts = lib_name.split(":")
        lib_path = os.path.join(self.LIBRARIES_DIR, lib_parts[0].replace(".", "/"), lib_parts[1], lib_parts[2])
        
        os.makedirs(lib_path, exist_ok=True)
        
        if "downloads" in lib and "artifact" in lib["downloads"]:
            artifact = lib["downloads"]["artifact"]
            dest_file = os.path.join(lib_path, os.path.basename(artifact["url"]))
            
            if os.path.exists(dest_file) and self.verify_file(dest_file, artifact["sha1"]):
                return True
            
            try:
                self.download_file(artifact["url"], dest_file, callback)
                
                if not self.verify_file(dest_file, artifact["sha1"]):
                    os.remove(dest_file)
                    return False
                
                return True
            
            except Exception as e:
                print(f"Error downloading library {lib_name}: {e}")
                return False
        
        return True
    
    def download_assets(self, version_info: Dict, callback) -> bool:
        """Download game assets."""
        assets_index = version_info["assetIndex"]
        
        # Download assets index
        index_url = assets_index["url"]
        index_sha1 = assets_index["sha1"]
        index_path = os.path.join(self.ASSETS_DIR, "indexes", f"{assets_index['id']}.json")
        
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        if not os.path.exists(index_path) or not self.verify_file(index_path, index_sha1):
            try:
                self.download_file(index_url, index_path, callback)
                
                if not self.verify_file(index_path, index_sha1):
                    os.remove(index_path)
                    return False
            except Exception as e:
                print(f"Error downloading assets index: {e}")
                return False
        
        # Download assets
        with open(index_path, "r", encoding="utf-8") as f:
            assets = json.load(f)
        
        for asset_name, asset_info in assets.get("objects", {}).items():
            try:
                if not self.download_asset(asset_name, asset_info, callback):
                    return False
            except Exception as e:
                print(f"Error downloading asset {asset_name}: {e}")
                return False
        
        return True
    
    def download_asset(self, asset_name: str, asset_info: Dict, callback) -> bool:
        """Download a single asset file."""
        asset_hash = asset_info["hash"]
        asset_dir = os.path.join(self.ASSETS_DIR, "objects", asset_hash[:2])
        asset_path = os.path.join(asset_dir, asset_hash)
        
        os.makedirs(asset_dir, exist_ok=True)
        
        if os.path.exists(asset_path) and self.verify_file(asset_path, asset_hash):
            return True
        
        asset_url = f"https://resources.download.minecraft.net/{asset_hash[:2]}/{asset_hash}"
        
        try:
            self.download_file(asset_url, asset_path, callback)
            
            if not self.verify_file(asset_path, asset_hash):
                os.remove(asset_path)
                return False
            
            return True
        
        except Exception as e:
            print(f"Error downloading asset {asset_name}: {e}")
            return False
    
    def download_file(self, url: str, destination: str, callback=None):
        """Download a file with progress tracking."""
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if callback:
                            percentage = (downloaded / total_size) * 100 if total_size else 0
                            callback(percentage, f"Downloading {os.path.basename(destination)}")
    
    def verify_file(self, file_path: str, expected_sha1: str) -> bool:
        """Verify file SHA-1 hash."""
        import hashlib
        
        try:
            with open(file_path, "rb") as f:
                hash_obj = hashlib.sha1()
                
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
                
                return hash_obj.hexdigest().lower() == expected_sha1.lower()
        
        except Exception as e:
            print(f"Error verifying file {file_path}: {e}")
            return False
    
    def save_version_info(self, version_info: Dict):
        """Save version information to disk."""
        version_dir = os.path.join(self.VERSIONS_DIR, version_info["id"])
        os.makedirs(version_dir, exist_ok=True)
        
        with open(os.path.join(version_dir, f"{version_info['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(version_info, f, indent=2)
    
    def is_version_installed(self, version_id: str) -> bool:
        """Check if a version is installed."""
        version_dir = os.path.join(self.VERSIONS_DIR, version_id)
        version_jar = os.path.join(version_dir, f"{version_id}.jar")
        
        return os.path.exists(version_dir) and os.path.exists(version_jar)