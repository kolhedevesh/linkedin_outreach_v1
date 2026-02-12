"""Test script for Search API layer"""

import os
from dotenv import load_dotenv
from search_api import SearchAPIClient, search_web, search_linkedin_profiles

# Load environment variables
load_dotenv()

def test_google_search():
    """Test Google Custom Search"""
    print("\n=== Testing Google Custom Search ===")
    try:
        client = SearchAPIClient()
        results = client.search_google("Python programming", num_results=5)
        print(f"✓ Google search returned {len(results)} results")
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. {result['title'][:60]}...")
            print(f"     {result['link']}")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("  Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in .env")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")

def test_bing_search():
    """Test Bing Search"""
    print("\n=== Testing Bing Search ===")
    try:
        client = SearchAPIClient()
        results = client.search_bing("machine learning", num_results=5)
        print(f"✓ Bing search returned {len(results)} results")
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. {result['title'][:60]}...")
            print(f"     {result['link']}")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("  Set BING_SEARCH_KEY in .env")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")

def test_linkedin_search():
    """Test LinkedIn profile search"""
    print("\n=== Testing LinkedIn Profile Search ===")
    try:
        results = search_linkedin_profiles(
            role="Product Manager",
            industry="SaaS",
            location="San Francisco"
        )
        print(f"✓ LinkedIn search returned {len(results)} results")
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. {result['title'][:60]}...")
            print(f"     {result['link']}")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("  Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in .env")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")

def test_cache():
    """Test caching functionality"""
    print("\n=== Testing Cache ===")
    try:
        client = SearchAPIClient()
        
        # First search (should hit API)
        print("First search (API call):")
        results1 = client.search_google("test query", num_results=3)
        print(f"  Got {len(results1)} results")
        
        # Second search (should hit cache)
        print("Second search (should use cache):")
        results2 = client.search_google("test query", num_results=3)
        print(f"  Got {len(results2)} results")
        
        if results1 == results2:
            print("✓ Cache working correctly")
        else:
            print("✗ Cache results differ")
    except ValueError as e:
        print(f"⊘ Skipped (API not configured): {e}")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("Search API Layer - Test Suite")
    print("=" * 60)
    
    test_google_search()
    test_bing_search()
    test_linkedin_search()
    test_cache()
    
    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)
