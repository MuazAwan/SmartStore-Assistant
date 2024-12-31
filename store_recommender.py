from store_manager import StoreManager
import json
import os
from typing import List, Dict, Any

class StoreRecommender:
    def __init__(self):
        self.store_manager = StoreManager()
        self.categories = {
            "sports": ["equipment", "fitness", "sports", "gym", "athletic", "training"],
            "books": ["book", "read", "study", "academic", "novel", "textbook"],
            "beauty": ["haircut", "salon", "spa", "beauty", "makeup", "massage"],
            "coffee": ["coffee", "cafe", "drink", "pastry", "breakfast", "snack"]
        }

    async def get_user_requirements(self) -> str:
        print("\n=== Welcome to Store Finder ===")
        print("Please tell me what you're looking for today.")
        print("For example:")
        print("- I need a haircut and massage")
        print("- Looking for sports equipment")
        print("- Want to buy some books")
        print("- Need a coffee and quiet place to work\n")

        return input("Your needs: ")

    def analyze_requirements(self, user_input: str) -> List[Dict[str, float]]:
        user_input = user_input.lower()
        store_scores = []

        # Load all store configurations
        for store_name in self.store_manager.list_stores():
            config_path = os.path.join(self.store_manager.config_dir, f"{store_name}_config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                store_config = json.load(f)

            score = self._calculate_store_match(user_input, store_config)
            store_scores.append({
                "store_name": store_name,
                "score": score,
                "store_info": store_config["store_info"]
            })

        # Sort by score in descending order
        return sorted(store_scores, key=lambda x: x["score"], reverse=True)

    def _calculate_store_match(self, user_input: str, store_config: Dict) -> float:
        score = 0.0
        
        # Check store description match
        description = store_config["store_info"].get("description", "").lower()
        if any(keyword in description for keyword in user_input.split()):
            score += 0.5

        # Check services match
        for service in store_config.get("services", []):
            service_name = service.get("name", "").lower()
            service_desc = service.get("description", "").lower()
            
            if any(keyword in service_name for keyword in user_input.split()):
                score += 1.0
            if any(keyword in service_desc for keyword in user_input.split()):
                score += 0.5

        return score

    def recommend_stores(self, scores: List[Dict[str, float]], top_n: int = 3) -> List[Dict[str, Any]]:
        recommendations = []
        
        for store in scores[:top_n]:
            if store["score"] > 0:
                recommendations.append({
                    "store_name": store["store_name"],
                    "store_info": store["store_info"],
                    "match_score": store["score"]
                })
                
        return recommendations

    def format_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        if not recommendations:
            return "I couldn't find any stores matching your requirements. Could you please be more specific?"

        result = "\n=== Recommended Stores ===\n"
        for i, rec in enumerate(recommendations, 1):
            result += f"\n{i}. {rec['store_info']['name']}"
            result += f"\n   {rec['store_info']['description']}"
            result += f"\n   Address: {rec['store_info']['address']}"
            result += f"\n   Hours: {rec['store_info']['hours']}"
            result += f"\n   Phone: {rec['store_info']['phone']}\n"

        return result 