from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from typing import Dict, Any, List
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from tools import ShoppingCart

load_dotenv()

class RenkoChatAgent:
    def __init__(self, store_name: str):
        """Initialize the chat agent for a specific store"""
        self.store_name = store_name
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        # Initialize paths
        self.base_path = os.getcwd()
        self.config_dir = os.path.join(self.base_path, "config", "store_configs")
        
        # Create store-specific chat history directory
        self.chat_histories_dir = os.path.join(self.base_path, "chat_histories", self.store_name)
        os.makedirs(self.chat_histories_dir, exist_ok=True)
        
        self.store_data = self._load_store_data()
        self.conversation_history: List[Dict[str, str]] = []
        self.prompt_template = self._create_prompt_template()
        self.shopping_cart = ShoppingCart()
        
        # Include store name in chat history filename
        self.chat_history_file = f"{self.store_name}_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def _load_store_data(self) -> Dict[str, Any]:
        """Load store-specific configuration and data"""
        config_path = os.path.join(self.config_dir, f"{self.store_name}_config.json")
        try:
            if not os.path.exists(config_path):
                print(f"Config path does not exist: {config_path}")
                return {"store_info": {}, "services": []}
                
            with open(config_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading store data: {str(e)}")
            return {"store_info": {}, "services": []}

    def _create_prompt_template(self) -> PromptTemplate:
        """Create the base prompt template for the store"""
        template = """You are a helpful assistant for {store_name}. 

        Store Information:
        {store_info}
        
        Available Services:
        {services}
        
        Shopping Cart:
        {cart_status}
        
        Previous Conversation:
        {conversation_history}
        
        Current Query: {query}
        
        Please provide a helpful, professional response. For cart operations, use these commands:
        - To add: "ADD_TO_CART: service_name"
        - To remove: "REMOVE_FROM_CART: service_name"
        - To view cart: "VIEW_CART"
        - To get total: "GET_TOTAL"
        """
        
        return PromptTemplate.from_template(template)

    async def handle_query(self, query: str) -> str:
        """Process customer query and return response"""
        try:
            # Handle cart operations
            if query.lower().startswith(("add", "remove", "view cart", "total")):
                return self._handle_cart_operation(query)
            
            # Format conversation history
            conversation_str = self._format_conversation_history()
            
            # Prepare prompt
            store_info = json.dumps(self.store_data.get("store_info", {}), indent=2)
            services = json.dumps(self.store_data.get("services", []), indent=2)
            cart_status = self.shopping_cart.view_cart()
            
            formatted_prompt = self.prompt_template.format(
                store_name=self.store_name,
                store_info=store_info,
                services=services,
                cart_status=cart_status,
                conversation_history=conversation_str,
                query=query
            )
            
            # Get response
            messages = [{"role": "user", "content": formatted_prompt}]
            response = await self.llm.ainvoke(messages)
            response_content = response.content
            
            # Add to conversation history with timestamp
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": query,
                "assistant": response_content
            })
            
            # Save after each interaction
            self.save_chat_history()
            
            return response_content
        
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again."

    def _handle_cart_operation(self, query: str) -> str:
        """Handle shopping cart operations"""
        query = query.lower()
        services = self.store_data.get("services", [])
        
        if query.startswith("add"):
            service_name = query.split("add")[1].strip()
            for service in services:
                if service["name"].lower() == service_name:
                    return self.shopping_cart.add_item(
                        service["name"],
                        service["price"]
                    )
            return f"Service '{service_name}' not found"
            
        elif query.startswith("remove"):
            service_name = query.split("remove")[1].strip()
            return self.shopping_cart.remove_item(service_name)
            
        elif "view cart" in query:
            return self.shopping_cart.view_cart()
            
        elif "total" in query:
            return f"Total: ${self.shopping_cart.get_total():.2f}"
            
        return "Invalid cart operation"

    async def get_service_info(self, service_name: str) -> Dict[str, Any]:
        """Get specific service information"""
        services = self.store_data.get("services", [])
        for service in services:
            if service["name"].lower() == service_name.lower():
                return service
        return {}

    async def check_availability(self, service_name: str, date: str) -> bool:
        """Check service availability for a specific date"""
        # This is a placeholder - implement actual availability check
        return True 

    def save_chat_history(self):
        """Save chat history to JSON file"""
        if not self.conversation_history:
            return  # Don't save empty conversations
            
        chat_data = {
            "store_name": self.store_name,
            "store_info": self.store_data.get("store_info", {}),
            "session_start": datetime.now().isoformat(),
            "conversation": self.conversation_history
        }
        
        file_path = os.path.join(self.chat_histories_dir, self.chat_history_file)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, indent=2, ensure_ascii=False)
            print(f"\nChat history saved to: {file_path}")
        except Exception as e:
            print(f"Error saving chat history: {str(e)}")

    def load_chat_histories(self) -> List[Dict[str, Any]]:
        """Load all chat histories for this store"""
        histories = []
        try:
            for filename in os.listdir(self.chat_histories_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.chat_histories_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        histories.append(json.load(f))
        except Exception as e:
            print(f"Error loading chat histories: {str(e)}")
        return histories

    def _format_conversation_history(self) -> str:
        """Format the conversation history for the prompt"""
        if not self.conversation_history:
            return "No previous conversation."
        
        formatted_history = []
        for entry in self.conversation_history:
            formatted_history.append(f"User: {entry['user']}")
            formatted_history.append(f"Assistant: {entry['assistant']}")
            if 'store_data' in entry:
                formatted_history.append(f"Context: {entry['store_data']}")
        
        return "\n".join(formatted_history)