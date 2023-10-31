import json
from utils.llm_tools import call_openai

# Set up logging
from utils.logger import logger  

def synthesize_main_answer(all_search_results: list, all_hypotheses: list) -> str:
    """
    Synthesizes the main answer from all the search results and hypotheses.
    """
    # Collate content from search results and hypotheses
    search_contents = [result['content'] for result in all_search_results]
    hypotheses_str = " ".join(all_hypotheses)

    # Prepare the prompt for LLM with detailed instructions, example, and constraints
    prompt = {
        "role": "system",
        "content": f'''
        Synthesize a comprehensive answer based on the following data:

        Search Results: {search_contents}
        Hypotheses: {hypotheses_str}

        Your response should integrate the information from the search results and hypotheses into a clear, well-structured, and concise answer. It should reflect a deep understanding of the topic, drawing connections and insights from the accumulated data.

        ---
        Example Prompt:
            Search Results: ["...effect of greenhouse gases...", "...rising global temperatures...", "...impact on polar ice caps..."]
            Hypotheses: ["Increased greenhouse gases might be accelerating the melting of polar ice caps."]

        Example Answer: 
            "The accumulation of greenhouse gases in the Earth's atmosphere is likely contributing to a rise in global temperatures, which in turn accelerates the melting of polar ice caps, leading to rising sea levels and potential impacts on global climate patterns."
        ---

        Formulate an answer that is informative, accurate, and provides a synthesis of the information given.
        '''
    }

    # Call LLM to synthesize the main answer
    try:
        response = json.loads(call_openai(messages=[prompt]))
        main_answer = response.get("content", "")
        return main_answer.strip()
    except Exception as err:
        logger.error(f"Error in synthesizing main answer: {err}")
        raise

