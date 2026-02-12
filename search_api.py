"""
Search API Layer using SerpAPI - Fetches public web results from Google/Bing
Handles caching, error handling, and result normalization
"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class SearchAPIClient:
    """Client for fetching web search results using SerpAPI"""
    
    def __init__(self, serpapi_key: Optional[str] = None):
        """
        Initialize Search API Client with SerpAPI
        
        Args:
            serpapi_key: SerpAPI key (defaults to env var SERPAPI_KEY)
        """
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_KEY")
        if not self.serpapi_key:
            raise ValueError("SERPAPI_KEY not found. Set it in .env file")
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache TTL
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key from query"""
        return f"search_{hash(query)}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in self.cache:
            return False
        cached_time, _ = self.cache[cache_key]
        return datetime.now() - cached_time < timedelta(seconds=self.cache_ttl)
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search using SerpAPI Google Search
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        # Check cache first
        cache_key = self._get_cache_key(query)
        if self._is_cache_valid(cache_key):
            _, cached_results = self.cache[cache_key]
            print(f"[CACHE HIT] Using cached results for: {query}")
            return cached_results
        
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.serpapi_key,
            "engine": "google",
            "num": min(num_results, 100),
            "gl": "us"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # Parse organic results
            for item in data.get("organic_results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "google"
                })
            
            # Cache results
            self.cache[cache_key] = (datetime.now(), results)
            print(f"[SEARCH] Found {len(results)} results for: {query}")
            return results
        
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] SerpAPI Google Search failed: {str(e)}")
            raise
    
    def search_bing(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search using SerpAPI Bing Search
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        # Check cache first
        cache_key = f"bing_{self._get_cache_key(query)}"
        if self._is_cache_valid(cache_key):
            _, cached_results = self.cache[cache_key]
            print(f"[CACHE HIT] Using cached Bing results for: {query}")
            return cached_results
        
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.serpapi_key,
            "engine": "bing",
            "num": min(num_results, 100)
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # Parse organic results
            for item in data.get("organic_results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "bing"
                })
            
            # Cache results
            self.cache[cache_key] = (datetime.now(), results)
            print(f"[SEARCH] Found {len(results)} Bing results for: {query}")
            return results
        
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] SerpAPI Bing Search failed: {str(e)}")
            raise
    
    def search_linkedin_profiles(self, role: str, industry: str, location: str) -> List[Dict]:
        """
        Search for LinkedIn profiles matching criteria
        Uses SerpAPI with LinkedIn site restriction
        
        Args:
            role: Job role/title
            industry: Industry
            location: Geographic location
            
        Returns:
            List of LinkedIn profile results
        """
        query = f'site:linkedin.com/in {role} {industry} {location}'
        print(f"[SEARCH] Querying LinkedIn profiles: {query}")
        return self.search_google(query, num_results=10)
    
    def clear_cache(self):
        """Clear all cached results"""
        self.cache.clear()
        print("[CACHE] Cleared all search results")


# Convenience functions
def search_web(query: str, provider: str = "google", num_results: int = 10) -> List[Dict]:
    """
    Quick web search without explicit client initialization
    
    Args:
        query: Search query
        provider: "google" or "bing"
        num_results: Number of results
        
    Returns:
        List of search results
    """
    client = SearchAPIClient()
    if provider.lower() == "google":
        return client.search_google(query, num_results)
    elif provider.lower() == "bing":
        return client.search_bing(query, num_results)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'google' or 'bing'")


def search_linkedin_profiles(role: str, industry: str, location: str) -> List[Dict]:
    """
    Search LinkedIn profiles matching criteria
    
    Args:
        role: Job role/title
        industry: Industry
        location: Geographic location
        
    Returns:
        List of LinkedIn profile results
    """
    client = SearchAPIClient()
    return client.search_linkedin_profiles(role, industry, location)
