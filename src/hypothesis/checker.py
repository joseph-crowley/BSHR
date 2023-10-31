import json
from utils.llm_tools import call_openai

# Set up logging
from utils.logger import logger  

def check_satisficed(main_query: str, all_search_results: list, all_hypotheses: list) -> bool:
    """
    Checks if the query has been satisfactorily addressed by the current search results and hypotheses.
    """
    # Prepare the prompt for LLM
    prompt = {
        "role": "system",
        "content": f'''
        Determine if the following query has been satisfactorily addressed:

        Query: {main_query}
        Search Results: {[result['content'] for result in all_search_results]}
        Hypotheses: {all_hypotheses}

        Answer "yes" if the query has been addressed thoroughly and no significant information is likely missing. Otherwise, answer "no".
        '''
    }

    try:
        response = json.loads(call_openai(messages=[prompt]))
        answer = response.get("content", "").strip().lower()

        if answer == "yes":
            return True
        elif answer == "no":
            return False
        else:
            raise ValueError(f"Invalid response from LLM: {answer}")
    except Exception as err:
        logger.error(f"Error in checking if query is satisficed: {err}")
        raise

def check_exhausted(main_query: str, all_search_results: list) -> bool:
    """
    Determines if further searching is likely to yield additional useful information.
    """
    # Prepare the prompt for LLM
    prompt = {
        "role": "system",
        "content": f'''
        Assess if additional searching will likely yield more useful information for the following query:

        Query: {main_query}
        Search Results: {[result['content'] for result in all_search_results]}

        Answer "yes" if you think all useful search avenues have been exhausted. Otherwise, answer "no".
        '''
    }

    try:
        response = json.loads(call_openai(messages=[prompt]))
        answer = response.get("content", "").strip().lower()

        if answer == "yes":
            return True
        elif answer == "no":
            return False
        else:
            raise ValueError(f"Invalid response from LLM: {answer}")
    except Exception as err:
        logger.error(f"Error in checking if search is exhausted: {err}")
        raise

