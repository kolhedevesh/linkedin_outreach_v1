from search_api import SearchAPIClient

def search_linkedin_profiles(role, industry, location):
    """
    Search for LinkedIn profiles using the Search API layer
    
    Args:
        role: Job role/title
        industry: Industry
        location: Geographic location
        
    Returns:
        List of LinkedIn profile results with title, link, snippet
    """
    client = SearchAPIClient()
    results = client.search_linkedin_profiles(role, industry, location)
    return results
