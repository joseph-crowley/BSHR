import requests
from typing import List, Dict
import json
import re
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

# Function to search Wikipedia for a summary of the given query
def search_wikipedia(query: str, sentences: int = 3) -> Dict:
    '''
    Search Wikipedia for a summary of the given query.
    '''
    endpoint = "https://en.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'srlimit': 1,  # You can adjust the limit for number of results
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        search_results = data.get('query', {}).get('search', [])
        if not search_results:
            return {'query': query, 'source': 'Wikipedia', 'content': None}

        # Get the title of the first result
        title = search_results[0].get('title')
        pageid = search_results[0].get('pageid')

        # Fetching the summary of the page
        summary_params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
            'pageids': pageid
        }

        summary_response = requests.get(endpoint, params=summary_params)
        summary_response.raise_for_status()
        summary_data = summary_response.json()
        summary = summary_data.get('query', {}).get('pages', {}).get(str(pageid), {}).get('extract', '')

        # Truncating the summary to the desired number of sentences
        truncated_summary = ' '.join(re.split(r'(?<=[.:;])\s', summary)[:sentences])

        return {
            'query': query,
            'source': 'Wikipedia',
            'title': title,
            'content': summary
        }
    except Exception as e:
        print(f"Error occurred while searching Wikipedia for '{query}': {e}")
        return {
            'query': query,
            'source': 'Wikipedia',
            'content': None
        }

# Function to execute searches for a list of queries
def execute_searches(queries: List[str], use_wiki=True) -> List[Dict]:
    ''' 
    Execute searches for a list of queries.
    '''
    if config.settings.BING_SEARCH_V7_SUBSCRIPTION_KEY == '' or config.settings.BING_SEARCH_V7_ENDPOINT == 'YOUR_KEY_HERE':
        results = [search_wikipedia(query) for query in queries]
    else:
        results = [execute_search(query) for query in queries]

    # make sure results are not too large (8192 tokens ~ 16k characters)
    count = 0
    for i_result, result in enumerate(results):
        i_result += 1
        if result['content'] is not None:
            count += len(result['content'].split())

        if count > 10000:
            break

    return results[:i_result]
