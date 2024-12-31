from typing import Dict, Any, List
import json
import os
from datetime import datetime
from base_agent import RenkoChatAgent

class StoreManager:
    def __init__(self):
        self.stores: Dict[str, RenkoChatAgent] = {}
        self.config_dir = os.path.join(os.getcwd(), "config", "store_configs")
        os.makedirs(self.config_dir, exist_ok=True)  # Create config directory if it doesn't exist

    def _load_existing_stores(self):
        """Load all existing store configurations"""
        if not os.path.exists(self.config_dir):
            return
            
        for config_file in os.listdir(self.config_dir):
            if config_file.endswith('_config.json'):
                store_name = config_file.replace('_config.json', '')
                try:
                    self.stores[store_name] = RenkoChatAgent(store_name)
                    print(f"Loaded existing store: {store_name}")
                except Exception as e:
                    print(f"Error loading store {store_name}: {str(e)}")

    def create_store(self, store_name: str, store_info: Dict[str, Any], services: List[Dict[str, Any]]) -> RenkoChatAgent:
        """Create a new store with its chatbot"""
        # Create store configuration
        config = {
            "store_info": store_info,
            "services": services,
            "created_at": datetime.now().isoformat()
        }

        # Save store configuration
        config_path = os.path.join(self.config_dir, f"{store_name}_config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Create and store chatbot instance
        self.stores[store_name] = RenkoChatAgent(store_name)
        print(f"Created new store and chatbot: {store_name}")
        
        return self.stores[store_name]

    def get_store_chatbot(self, store_name: str) -> RenkoChatAgent:
        """Get chatbot for existing store"""
        if store_name not in self.stores:
            # Try to load the store if it exists
            config_path = os.path.join(self.config_dir, f"{store_name}_config.json")
            if os.path.exists(config_path):
                self.stores[store_name] = RenkoChatAgent(store_name)
            else:
                raise ValueError(f"Store {store_name} does not exist")
        return self.stores[store_name]

    def list_stores(self) -> List[str]:
        """List all available stores"""
        # Refresh store list from config directory
        store_files = [f.replace('_config.json', '') 
                      for f in os.listdir(self.config_dir) 
                      if f.endswith('_config.json')]
        return store_files

    def delete_store(self, store_name: str):
        """Delete a store and its configuration"""
        config_path = os.path.join(self.config_dir, f"{store_name}_config.json")
        if os.path.exists(config_path):
            os.remove(config_path)
            if store_name in self.stores:
                del self.stores[store_name]
            print(f"Deleted store: {store_name}")
        else:
            raise ValueError(f"Store {store_name} does not exist") 