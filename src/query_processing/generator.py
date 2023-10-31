import json
import ast

from utils.llm_tools import call_openai

# Set up logging
from utils.logger import logger  

# Function to extract keywords using LLM
def extract_keywords(query: str, existing_keywords: list) -> list:
    """
    Extracts keywords from a given query using LLM.
    """
    system_msg = {
        "role": "system",
        "content": f'Reply with a list of key words based on the following query:\n\n{query}\n\nCurrent keywords: {existing_keywords}\n\nGenerate new keywords that approach the query from another perspective and clearly fit the query.\n\n---\n\nExample:\nQuery: What is the history of the United States?\n["history of United States", "American revolution", "founding USA", "1776", "13 colonies"]\n\nReply only with the list of keywords, and no other text.',
    }

    usr_msg = {
        "role": "user",
        "content": query,
    }

    conversation = [system_msg, usr_msg]
    response = json.loads(call_openai(
        messages=conversation,
    ))

    try:
        new_keywords = ast.literal_eval(response["content"])
        return new_keywords
    except Exception as err:
        logger.error(f"Error: {err}")
        logger.error(f"Response: {response}")
        raise

# Function to create combinations of keywords
def create_queries(keywords: list) -> list:
    """
    Creates combinations of keywords as queries using LLM.
    """

    system_msg = {
        "role": "system",
        "content": f'Reply with a list of queries based on the following keywords:\n\n{keywords}\n\nGenerate queries that approach the keywords from another perspective and clearly fit the keywords.\n\n---\n\nExample:\nKeywords: ["history of United States", "American revolution", "founding USA", "1776", "13 colonies"]\n["history of United States", "American revolution", "founding USA", "1776", "13 colonies", "history of the American revolution", "history of the founding of the USA", "history of 1776", "history of the 13 colonies", "American revolution of 1776", "American revolution of the 13 colonies", "founding of the USA in 1776", "founding of the USA in the 13 colonies", "1776 American revolution", "1776 founding of the USA", "1776 13 colonies", "13 colonies American revolution", "13 colonies founding of the USA", "13 colonies 1776"]\n\nReply only with the list of queries, and no other text.',
    }

    usr_msg = {
        "role": "user",
        "content": ', '.join(keywords),
    }

    conversation = [system_msg, usr_msg]

    response = json.loads(call_openai(
        messages=conversation,
    ))

    try:
        new_queries = ast.literal_eval(response["content"])
        return new_queries
    except Exception as err:
        logger.error(f"Error: {err}")
        logger.error(f"Response: {response}")
        raise

# Function to generate search queries
def generate_search_queries(main_query: str, existing_keywords: list, all_search_results: list, all_hypotheses: list) -> list:
    """
    Generates new search queries based on the query, keywords, search results, and existing hypotheses.
    """

    new_keywords = extract_keywords(main_query, existing_keywords)
    all_keywords = list(set(existing_keywords + new_keywords))
    new_queries = create_queries(all_keywords)

    logger.info(f"New keywords: {new_keywords}")

    return new_queries
