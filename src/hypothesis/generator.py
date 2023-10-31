import json
from utils.llm_tools import call_openai

# Set up logging
from utils.logger import logger  

def generate_new_hypothesis(main_query: str, all_search_results: list, existing_hypotheses: list) -> str:
    """
    Generates a new hypothesis based on the main query, all search results, and existing hypotheses.
    """
    # Collate data from search results and existing hypotheses
    search_contents = [result['content'] for result in all_search_results]

    # Prepare the prompt for LLM with detailed instructions, example, and constraints
    prompt = {
        "role": "system",
        "content": f'''
        Generate a hypothesis based on the following data:

        Query: {main_query}
        Search Results: {search_contents}
        Existing Hypotheses: {existing_hypotheses}

        Your hypothesis should be concise, relevant, and insightful. Avoid repeating information already contained in the search results or existing hypotheses. Instead, focus on synthesizing the information into a new perspective or idea that is not immediately obvious.

        ---
        Example Prompt:
            Query: What is the impact of climate change on polar bears?
            Search Results: ["...declining sea ice...", "...changes in prey availability...", "...increase in polar bear-human interactions..."]
            Existing Hypotheses: ["Climate change may be forcing polar bears to adapt new hunting strategies."]

        Example Response: 
            "Climate change is not only altering polar bear habitats but might also be influencing polar bear behavior and social structures."
        ---

        Based on the information provided, formulate a new hypothesis that is distinct, yet grounded in the data given.
        '''
    }

    # Call LLM to generate a new hypothesis
    try:
        response = json.loads(call_openai(messages=[prompt]))
        new_hypothesis = response.get("content", "")
        return new_hypothesis.strip()
    except Exception as err:
        logger.error(f"Error in generating new hypothesis: {err}")
        raise

