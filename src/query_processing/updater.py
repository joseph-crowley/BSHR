from typing import List, Dict

# Set up logging
from utils.logger import logger  

def update_search_results(all_search_results: List[Dict], new_search_results: List[Dict]) -> None:
    """
    Updates the list of all search results with new search results, avoiding duplicates.

    :param all_search_results: List of dictionaries representing all accumulated search results.
    :param new_search_results: List of dictionaries representing new search results to be added.
    """
    try:
        existing_queries = {result['query'] for result in all_search_results}

        for result in new_search_results:
            if 'query' not in result or not isinstance(result, dict):
                logger.warning(f"Invalid result format: {result}")
                continue

            if result['query'] not in existing_queries:
                all_search_results.append(result)
                existing_queries.add(result['query'])

    except Exception as e:
        logger.error(f"Error updating search results: {e}")
        raise

