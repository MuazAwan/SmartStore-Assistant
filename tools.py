from langchain.tools import Tool
from langchain.agents import Tool
from typing import Dict, List, Optional
import aiohttp
from pydantic import BaseModel

class CartItem(BaseModel):
    service_name: str
    price: float
    quantity: int = 1

class ShoppingCart:
    def __init__(self):
        self.items: List[CartItem] = []
        
    def add_item(self, service_name: str, price: float, quantity: int = 1) -> str:
        """Add a service to the cart"""
        # Check if service already exists in cart
        for item in self.items:
            if item.service_name.lower() == service_name.lower():
                item.quantity += quantity
                return f"Updated {service_name} quantity to {item.quantity}"
        
        # Add new item
        new_item = CartItem(service_name=service_name, price=price, quantity=quantity)
        self.items.append(new_item)
        return f"Added {service_name} to cart"
    
    def remove_item(self, service_name: str, quantity: Optional[int] = None) -> str:
        """Remove a service from the cart"""
        for i, item in enumerate(self.items):
            if item.service_name.lower() == service_name.lower():
                if quantity is None or item.quantity <= quantity:
                    self.items.pop(i)
                    return f"Removed {service_name} from cart"
                else:
                    item.quantity -= quantity
                    return f"Updated {service_name} quantity to {item.quantity}"
        return f"Service {service_name} not found in cart"
    
    def get_total(self) -> float:
        """Calculate total price of items in cart"""
        return sum(item.price * item.quantity for item in self.items)
    
    def view_cart(self) -> str:
        """Display cart contents"""
        if not self.items:
            return "Cart is empty"
        
        cart_view = "Shopping Cart:\n"
        for item in self.items:
            cart_view += f"- {item.service_name}: ${item.price} x {item.quantity} = ${item.price * item.quantity}\n"
        cart_view += f"\nTotal: ${self.get_total():.2f}"
        return cart_view

class RenkoTools:
    def __init__(self, store_name: str, api_base_url: str):
        self.store_name = store_name
        self.api_base_url = api_base_url
        
    async def check_availability(self, service_id: str, date: str) -> Dict:
        """Check service availability for a specific date"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_base_url}/stores/{self.store_name}/availability"
            async with session.get(url, params={"service_id": service_id, "date": date}) as response:
                return await response.json()

    async def create_booking(self, service_id: str, date: str, user_id: str) -> Dict:
        """Create a new booking"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_base_url}/stores/{self.store_name}/bookings"
            data = {
                "service_id": service_id,
                "date": date,
                "user_id": user_id
            }
            async with session.post(url, json=data) as response:
                return await response.json()

    def get_tools(self) -> List[Tool]:
        """Return list of available tools for the agent"""
        return [
            Tool(
                name="check_availability",
                func=self.check_availability,
                description="Check service availability for a specific date"
            ),
            Tool(
                name="create_booking",
                func=self.create_booking,
                description="Create a new booking for a service"
            )
        ] 