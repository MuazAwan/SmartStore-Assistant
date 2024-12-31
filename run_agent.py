from store_recommender import StoreRecommender
from store_manager import StoreManager
import asyncio

async def main():
    recommender = StoreRecommender()
    store_manager = StoreManager()

    while True:
        # Get user requirements
        user_input = await recommender.get_user_requirements()
        
        if user_input.lower() == 'quit':
            print("Thank you for using our service. Goodbye!")
            break

        # Analyze and get recommendations
        scores = recommender.analyze_requirements(user_input)
        recommendations = recommender.recommend_stores(scores)
        
        # Show recommendations
        print(recommender.format_recommendations(recommendations))
        
        # Ask if user wants to chat with a specific store
        if recommendations:
            while True:
                choice = input("\nWould you like to chat with any of these stores? (Enter store number or 'no'): ")
                
                if choice.lower() == 'no':
                    break
                    
                try:
                    store_index = int(choice) - 1
                    if 0 <= store_index < len(recommendations):
                        store_name = recommendations[store_index]["store_name"]
                        agent = store_manager.get_store_chatbot(store_name)
                        
                        print(f"\n=== Chatting with {recommendations[store_index]['store_info']['name']} ===")
                        print("Type 'quit' to exit chat, 'history' to see conversation history")
                        print("-" * 50 + "\n")
                        
                        while True:
                            query = input("Your question: ")
                            if query.lower() == 'quit':
                                break
                            elif query.lower() == 'history':
                                print("\nConversation History:")
                                for entry in agent.conversation_history:
                                    print(f"User: {entry['user']}")
                                    print(f"Assistant: {entry['assistant']}\n")
                                continue
                                
                            response = await agent.handle_query(query)
                            print(f"Assistant: {response}\n")
                        break
                    else:
                        print("Invalid store number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number or 'no'.")
        
        print("\nWould you like to look for something else?")

if __name__ == "__main__":
    asyncio.run(main()) 