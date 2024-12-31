from fastapi import FastAPI, HTTPException
from .base_agent import RenkoChatAgent
from ..monitoring.metrics import ChatbotMetrics
from ..cache.redis_cache import RedisCache
from typing import Dict
import os

app = FastAPI()
metrics = ChatbotMetrics()
cache = RedisCache(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379))
)

@app.post("/chat")
async def handle_chat(store_name: str, query: str):
    async with metrics.track_response_time(store_name):
        try:
            # Check cache first
            cached_response = await cache.get_cached_response(store_name, query)
            if cached_response:
                await metrics.track_request(store_name, "cache_hit")
                return {"response": cached_response}

            # Get response from chatbot
            response = await get_store_agent(store_name).handle_query(query)
            
            # Cache the response
            await cache.cache_response(store_name, query, response)
            
            await metrics.track_request(store_name, "success")
            return {"response": response}
            
        except Exception as e:
            await metrics.track_request(store_name, "error")
            raise HTTPException(status_code=500, detail=str(e)) 