import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


class CacheManager:
    """Caches LLM responses to avoid redundant API calls and tracks API costs."""
    
    CACHE_DIR = Path("./llm_cache")
    COST_FILE = Path("./llm_cache/costs.json")
    
    # Cost per 1K tokens (approximate)
    PROVIDER_COSTS = {
        "mistral": 0.00015,  # $0.15 per 1M input tokens
        "gemini": 0.0005,    # $0.50 per 1M input tokens
        "openai": 0.003,     # GPT-3.5 pricing
    }
    
    def __init__(self):
        """Initialize cache directory."""
        self.CACHE_DIR.mkdir(exist_ok=True)
    
    @staticmethod
    def _hash_query(system_prompt: str, human_message: str) -> str:
        """Create unique hash for a query combination."""
        combined = f"{system_prompt or ''}||{human_message or ''}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_cached_response(self, system_prompt: str, human_message: str):
        """
        Retrieve cached response if it exists.
        
        Args:
            system_prompt: The system prompt used
            human_message: The human message/query
            
        Returns:
            Cached response string if found, None otherwise
        """
        cache_hash = self._hash_query(system_prompt, human_message)
        cache_file = self.CACHE_DIR / f"{cache_hash}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                data = json.load(f)
            print(f"✅ Cache HIT! Retrieved from {cache_file.name}")
            return data['response']
        return None
    
    def save_response(self, system_prompt: str, human_message: str, response: str, tokens_used: int = 0):
        """
        Cache the response for future use.
        
        Args:
            system_prompt: The system prompt used
            human_message: The human message/query
            response: The LLM response to cache
            tokens_used: Number of tokens used (estimated)
        """
        cache_hash = self._hash_query(system_prompt, human_message)
        cache_file = self.CACHE_DIR / f"{cache_hash}.json"
        
        cache_data = {
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'tokens': tokens_used,
            'system_prompt_hash': cache_hash
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"💾 Response cached to {cache_file.name}")
    
    def track_cost(self, provider: str, tokens_used: int):
        """
        Track API costs by provider.
        
        Args:
            provider: The LLM provider name
            tokens_used: Number of tokens used
            
        Returns:
            Cost in USD
        """
        if not self.COST_FILE.exists():
            costs = {}
        else:
            with open(self.COST_FILE, 'r') as f:
                costs = json.load(f)
        
        cost = (tokens_used / 1000) * self.PROVIDER_COSTS.get(provider, 0.001)
        
        if provider not in costs:
            costs[provider] = {
                'total_cost': 0.0,
                'total_tokens': 0,
                'num_calls': 0
            }
        
        costs[provider]['total_cost'] += cost
        costs[provider]['total_tokens'] += tokens_used
        costs[provider]['num_calls'] += 1
        
        with open(self.COST_FILE, 'w') as f:
            json.dump(costs, f, indent=2)
        
        return cost
    
    def get_cost_summary(self):
        """
        Get summary of all API costs.
        
        Returns:
            Dictionary with cost information
        """
        if not self.COST_FILE.exists():
            return {"total_cost": 0.0, "providers": {}}
        
        with open(self.COST_FILE, 'r') as f:
            costs = json.load(f)
        
        total = sum(provider_data['total_cost'] for provider_data in costs.values())
        return {
            "total_cost": round(total, 4),
            "providers": costs
        }
    
    def clear_cache(self):
        """Clear all cached responses."""
        for file in self.CACHE_DIR.glob("*.json"):
            if file.name != "costs.json":
                file.unlink()
        print("🗑️  Cache cleared!")
