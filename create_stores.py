from store_manager import StoreManager
import os
import json

def create_diverse_stores():
    # Initialize store manager
    store_manager = StoreManager()
    
    # Ensure config directory exists
    config_dir = os.path.join(os.getcwd(), "config", "store_configs")
    os.makedirs(config_dir, exist_ok=True)
    
    # Store configurations
    stores_config = {
        "sports_hub": {
            "store_info": {
                "name": "Champion Sports Hub",
                "address": "123 Stadium Ave, City",
                "phone": "555-0123",
                "hours": "9 AM - 9 PM",
                "description": "Your one-stop shop for all sports equipment and gear",
                "return_policy": "30-day return with receipt",
                "warranty": "1-year warranty on equipment"
            },
            "services": [
                {
                    "name": "Basketball",
                    "price": 29.99,
                    "description": "Official size basketball",
                    "brands": ["Nike", "Spalding", "Wilson"]
                },
                {
                    "name": "Tennis Racket",
                    "price": 89.99,
                    "description": "Professional tennis racket",
                    "brands": ["Wilson", "Head", "Babolat"]
                },
                {
                    "name": "Running Shoes",
                    "price": 79.99,
                    "description": "High-performance running shoes",
                    "brands": ["Nike", "Adidas", "New Balance"]
                }
            ]
        },
        "bookstore": {
            "store_info": {
                "name": "Knowledge Corner",
                "address": "456 Library Lane, City",
                "phone": "555-0456",
                "hours": "10 AM - 8 PM",
                "description": "Wide collection of books across all genres",
                "membership": "Available with 10% discount",
                "online_ordering": "Available with home delivery"
            },
            "services": [
                {
                    "name": "Fiction Books",
                    "price": 19.99,
                    "description": "Latest fiction titles",
                    "categories": ["Mystery", "Romance", "Sci-Fi"]
                },
                {
                    "name": "Academic Books",
                    "price": 49.99,
                    "description": "Textbooks and reference materials",
                    "categories": ["Science", "Mathematics", "History"]
                },
                {
                    "name": "Book Binding",
                    "price": 20.00,
                    "description": "Professional book binding service"
                }
            ]
        },
        "beauty_salon": {
            "store_info": {
                "name": "Glamour Beauty Lounge",
                "address": "789 Fashion St, City",
                "phone": "555-0789",
                "hours": "8 AM - 7 PM",
                "description": "Premium beauty and wellness services",
                "appointment": "Online booking available",
                "cancellation_policy": "24-hour notice required"
            },
            "services": [
                {
                    "name": "Haircut & Styling",
                    "price": 45.00,
                    "description": "Professional haircut and styling",
                    "duration": "60 minutes"
                },
                {
                    "name": "Makeup Service",
                    "price": 75.00,
                    "description": "Professional makeup application",
                    "duration": "45 minutes"
                },
                {
                    "name": "Spa Package",
                    "price": 120.00,
                    "description": "Complete spa treatment package",
                    "duration": "120 minutes"
                }
            ]
        }
    }
    
    try:
        # Create config files for each store
        for store_name, config in stores_config.items():
            config_path = os.path.join(config_dir, f"{store_name}_config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"Created configuration file for {store_name}")
            
            # Create store using store manager
            store_manager.create_store(
                store_name,
                config["store_info"],
                config["services"]
            )
            print(f"Created {store_name} successfully!")
        
        # List all stores
        stores = store_manager.list_stores()
        print("\nAvailable stores:", stores)
        print("\nStore creation completed! You can now run the chatbot to interact with any store.")
        
    except Exception as e:
        print(f"Error creating stores: {str(e)}")
        raise

if __name__ == "__main__":
    create_diverse_stores() 