import requests
from typing import List, Dict
import json
import config.settings

# Function to execute a web search using Bing Search API
def execute_search(query: str) -> Dict:
    ''' 
    Execute a web search for a given query using Bing Web Search API.
    '''
    subscription_key = config.settings.BING_SEARCH_V7_SUBSCRIPTION_KEY
    endpoint = config.settings.BING_SEARCH_V7_ENDPOINT + "/v7.0/search"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'q': query, 'mkt': 'en-US'}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()

        # Extracting relevant information
        simplified_results = []
        for item in response_json.get('webPages', {}).get('value', []):
            simplified_result = {
                "description": item.get('snippet', ''),
                "source": item.get('url', '')
            }
        simplified_results.append(simplified_result)

        return {
            'query': query,
            'source': 'Bing Web Search API',
            'content': json.dumps(simplified_results)
        }
    except Exception as e:
        print(f"Error occurred while searching for '{query}': {e}")
        return {
            'query': query,
            'source': 'Bing Web Search API',
            'content': None
        }

# Function to execute searches for a list of queries
def execute_searches(queries: List[str]) -> List[Dict]:
    ''' 
    Execute searches for a list of queries.
    '''
    return [execute_search(query) for query in queries]
