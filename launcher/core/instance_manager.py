"""
Instance Management Module
"""

import os
import json
import shutil
from typing import Dict, List, Optional
import uuid
from dataclasses import dataclass, asdict

@dataclass
class Instance:
    """Represents a Minecraft instance configuration."""
    id: str
    name: str
    version: str
    type: str  # "vanilla", "forge", "fabric", "quilt"
    description: str
    icon: str
    last_played: float
    total_playtime: float
    modpack: Optional[str]
    java_args: List[str]
    custom_settings: Dict[str, Any]

class InstanceManager:
    """Manages Minecraft instances."""
    
    INSTANCES_DIR = "instances"
    INSTANCE_METADATA = "instance.json"
    
    def __init__(self):
        self.instances = self.load_instances()
    
    def load_instances(self) -> Dict[str, Instance]:
        """Load all instances from disk."""
        instances = {}
        
        if not os.path.exists(self.INSTANCES_DIR):
            os.makedirs(self.INSTANCES_DIR, exist_ok=True)
            return instances
        
        for instance_dir in os.listdir(self.INSTANCES_DIR):
            instance_path = os.path.join(self.INSTANCES_DIR, instance_dir)
            
            if os.path.isdir(instance_path):
                metadata_file = os.path.join(instance_path, self.INSTANCE_METADATA)
                
                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            instance = Instance(**data)
                            instances[instance.id] = instance
                    except Exception as e:
                        print(f"Error loading instance {instance_dir}: {e}")
        
        return instances
    
    def create_instance(self, name: str, version: str, instance_type: str = "vanilla", 
                       description: str = "", icon: str = "", modpack: Optional[str] = None) -> Instance:
        """Create a new instance."""
        instance_id = str(uuid.uuid4())
        instance_dir = os.path.join(self.INSTANCES_DIR, instance_id)
        
        os.makedirs(instance_dir, exist_ok=True)
        
        instance = Instance(
            id=instance_id,
            name=name,
            version=version,
            type=instance_type,
            description=description,
            icon=icon,
            last_played=0,
            total_playtime=0,
            modpack=modpack,
            java_args=[],
            custom_settings={}
        )
        
        self.save_instance(instance)
        self.instances[instance_id] = instance
        
        return instance
    
    def save_instance(self, instance: Instance):
        """Save instance configuration."""
        instance_dir = os.path.join(self.INSTANCES_DIR, instance.id)
        
        with open(os.path.join(instance_dir, self.INSTANCE_METADATA), "w", encoding="utf-8") as f:
            json.dump(asdict(instance), f, indent=2, ensure_ascii=False)
    
    def get_instance(self, instance_id: str) -> Optional[Instance]:
        """Get instance by ID."""
        return self.instances.get(instance_id)
    
    def get_all_instances(self) -> List[Instance]:
        """Get all instances."""
        return list(self.instances.values())
    
    def delete_instance(self, instance_id: str):
        """Delete an instance."""
        if instance_id in self.instances:
            instance_dir = os.path.join(self.INSTANCES_DIR, instance_id)
            
            try:
                shutil.rmtree(instance_dir)
                del self.instances[instance_id]
            except Exception as e:
                print(f"Error deleting instance {instance_id}: {e}")
    
    def update_instance(self, instance: Instance):
        """Update an existing instance."""
        if instance.id in self.instances:
            self.instances[instance.id] = instance
            self.save_instance(instance)
    
    def get_playtime(self, instance_id: str) -> float:
        """Get total playtime for an instance."""
        instance = self.get_instance(instance_id)
        return instance.total_playtime if instance else 0
    
    def increment_playtime(self, instance_id: str, seconds: float):
        """Increment instance playtime."""
        instance = self.get_instance(instance_id)
        
        if instance:
            instance.total_playtime += seconds
            instance.last_played = time.time()
            self.update_instance(instance)
    
    def launch_instance(self, instance_id: str, account: dict):
        """Launch a specific instance."""
        instance = self.get_instance(instance_id)
        
        if not instance:
            raise ValueError(f"Instance {instance_id} not found")
        
        # TODO: Implement actual instance launch
        instance.last_played = time.time()
        self.update_instance(instance)
        
        print(f"Launching instance: {instance.name}")
    
    def get_instance_path(self, instance_id: str) -> str:
        """Get instance directory path."""
        return os.path.join(self.INSTANCES_DIR, instance_id)
    
    def install_mod(self, instance_id: str, mod_file: str):
        """Install a mod to an instance."""
        instance = self.get_instance(instance_id)
        
        if not instance:
            raise ValueError(f"Instance {instance_id} not found")
        
        mod_dir = os.path.join(self.get_instance_path(instance_id), "mods")
        os.makedirs(mod_dir, exist_ok=True)
        
        try:
            shutil.copy(mod_file, mod_dir)
            print(f"Mod installed to instance: {instance.name}")
        except Exception as e:
            print(f"Error installing mod: {e}")
    
    def remove_mod(self, instance_id: str, mod_name: str):
        """Remove a mod from an instance."""
        instance = self.get_instance(instance_id)
        
        if not instance:
            raise ValueError(f"Instance {instance_id} not found")
        
        mod_path = os.path.join(self.get_instance_path(instance_id), "mods", mod_name)
        
        try:
            if os.path.exists(mod_path):
                os.remove(mod_path)
                print(f"Mod removed from instance: {instance.name}")
        except Exception as e:
            print(f"Error removing mod: {e}")