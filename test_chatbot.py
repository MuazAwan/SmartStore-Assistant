import asyncio
from store_manager import StoreManager
from store_recommender import StoreRecommender
import os
import json

class ChatbotTester:
    def __init__(self):
        self.store_manager = StoreManager()
        self.recommender = StoreRecommender()
        self.test_results = []

    async def run_all_tests(self):
        print("\n=== Starting Chatbot Tests ===\n")
        
        # Test 1: Store Creation and Configuration
        await self.test_store_creation()
        
        # Test 2: Store Recommendations
        await self.test_recommendations()
        
        # Test 3: Chat Functionality
        await self.test_chat_functionality()
        
        # Test 4: Chat History
        await self.test_chat_history()
        
        self.print_test_results()

    async def test_store_creation(self):
        print("Testing Store Creation...")
        try:
            # Check if stores exist
            stores = self.store_manager.list_stores()
            if not stores:
                self.test_results.append(("Store Creation", "FAILED", "No stores found"))
                return
            
            # Check store configurations
            for store_name in stores:
                config_path = os.path.join(self.store_manager.config_dir, f"{store_name}_config.json")
                if not os.path.exists(config_path):
                    self.test_results.append(("Store Config", "FAILED", f"Missing config for {store_name}"))
                    continue
                
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if "store_info" in config and "services" in config:
                        self.test_results.append(("Store Config", "PASSED", f"{store_name} configuration valid"))
                    else:
                        self.test_results.append(("Store Config", "FAILED", f"Invalid config for {store_name}"))
        
        except Exception as e:
            self.test_results.append(("Store Creation", "ERROR", str(e)))

    async def test_recommendations(self):
        print("Testing Store Recommendations...")
        test_queries = [
            "I need sports equipment",
            "Looking for books",
            "Need a haircut",
            "Want coffee"
        ]
        
        try:
            for query in test_queries:
                scores = self.recommender.analyze_requirements(query)
                recommendations = self.recommender.recommend_stores(scores)
                
                if recommendations:
                    self.test_results.append(("Recommendations", "PASSED", f"Query: {query} - Found {len(recommendations)} matches"))
                else:
                    self.test_results.append(("Recommendations", "WARNING", f"Query: {query} - No matches found"))
        
        except Exception as e:
            self.test_results.append(("Recommendations", "ERROR", str(e)))

    async def test_chat_functionality(self):
        print("Testing Chat Functionality...")
        test_questions = [
            "What are your hours?",
            "What services do you offer?",
            "How much do things cost?"
        ]
        
        try:
            stores = self.store_manager.list_stores()
            for store_name in stores[:1]:  # Test with first store
                agent = self.store_manager.get_store_chatbot(store_name)
                
                for question in test_questions:
                    response = await agent.handle_query(question)
                    if response and not response.startswith("I apologize"):
                        self.test_results.append(("Chat Response", "PASSED", f"{store_name}: Valid response to '{question}'"))
                    else:
                        self.test_results.append(("Chat Response", "WARNING", f"{store_name}: Potential issue with '{question}'"))
        
        except Exception as e:
            self.test_results.append(("Chat Functionality", "ERROR", str(e)))

    async def test_chat_history(self):
        print("Testing Chat History...")
        try:
            stores = self.store_manager.list_stores()
            for store_name in stores[:1]:  # Test with first store
                agent = self.store_manager.get_store_chatbot(store_name)
                
                # Send test message
                await agent.handle_query("Test message")
                
                # Check if history file was created
                if os.path.exists(agent.chat_histories_dir):
                    files = os.listdir(agent.chat_histories_dir)
                    if files:
                        self.test_results.append(("Chat History", "PASSED", f"{store_name}: History files created"))
                    else:
                        self.test_results.append(("Chat History", "FAILED", f"{store_name}: No history files found"))
                else:
                    self.test_results.append(("Chat History", "FAILED", f"{store_name}: History directory not found"))
        
        except Exception as e:
            self.test_results.append(("Chat History", "ERROR", str(e)))

    def print_test_results(self):
        print("\n=== Test Results ===\n")
        for test_name, status, message in self.test_results:
            status_color = {
                "PASSED": "\033[92m",  # Green
                "FAILED": "\033[91m",  # Red
                "WARNING": "\033[93m",  # Yellow
                "ERROR": "\033[91m"     # Red
            }.get(status, "")
            reset_color = "\033[0m"
            print(f"{test_name}: {status_color}{status}{reset_color} - {message}")

async def main():
    tester = ChatbotTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 