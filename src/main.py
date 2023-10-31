import sys
import os
import json

# Import the custom logger
from utils.logger import logger

# Add the project config to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from query_processing.generator import generate_search_queries
from query_processing.executor import execute_searches
from query_processing.updater import update_search_results
from hypothesis.generator import generate_new_hypothesis
from hypothesis.checker import check_satisficed, check_exhausted
from hypothesis.synthesizer import synthesize_main_answer

def bshr_loop(query):
    logger.info("Started the BSHR loop with query: {}".format(query))
    all_keywords = []  # list of lists of strings
    all_search_results = []  # list of dicts with "query", "source", and "content"
    all_hypotheses = []  # list of strings
    try:
        while True:
            logger.debug("Starting new iteration of BSHR loop.")

            # debug the current loop state
            logger.debug("Keywords: {}".format(all_keywords))
            logger.debug("Search results: {}".format(all_search_results))
            logger.debug("Hypotheses: {}".format(all_hypotheses))

            # Step 1: Brainstorm
            logger.info("Generating search queries.")
            search_queries = generate_search_queries(query, all_keywords, all_search_results, all_hypotheses)
            
            # Step 2: Search
            logger.info("Executing searches.")
            new_search_results = execute_searches(search_queries)
            logger.info("Updating search results.")
            update_search_results(all_search_results, new_search_results)
            
            # Step 3: Hypothesize
            logger.info("Generating new hypothesis.")
            new_hypothesis = generate_new_hypothesis(query, all_search_results, all_hypotheses)
            all_hypotheses.append(new_hypothesis)
            
            # Step 4: Refine
            logger.info("Checking if the hypotheses are satisficed or if the search is exhausted.")
            if check_satisficed(query, all_search_results, all_hypotheses):
                logger.info("Hypotheses satisficed. Exiting loop.")
                return all_search_results, all_hypotheses
            
            if check_exhausted(query, all_search_results):
                logger.warning("Search exhausted. Exiting loop.")
                return all_search_results, all_hypotheses
    except Exception as e:
        logger.error("Exception occurred in BSHR loop: {}".format(e))
        raise e

if __name__ == '__main__':
    logger.info("Starting main application loop.")
    try:
        while True:
            main_query = input('\n\n\n#########\n\n\nEnter a query to ponder ("exit" to quit): \n    ')
            if main_query.lower() == 'exit':
                logger.info("Exit command received. Shutting down.")
                break

            print('\n\n\n#########\nProcessing your query...\n\n\n')
            
            logger.info("Processing query: {}".format(main_query))
            evidence, hypotheses = bshr_loop(main_query)
            answer = synthesize_main_answer(evidence, hypotheses)
            print('\n\n\nResults:\n\n\n', answer)

            evidence_q = input('\n\n\nWould you like to see the evidence? [Y/n] ')
            if evidence_q.lower() == 'y' or evidence_q == '':
                print('\n\n\nEVIDENCE:\n\n\n', json.dumps(evidence, indent=4))

            hypotheses_q = input('\n\n\nWould you like to see the hypotheses? [Y/n] ')

            if hypotheses_q.lower() == 'y' or hypotheses_q == '':
                print('\n\n\nHYPOTHESES:\n\n\n', json.dumps(hypotheses, indent=4))

    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt received. Exiting.")
    except Exception as e:
        logger.critical("An unexpected error occurred: {}".format(e))
        raise e
    finally:
        logger.info("Application shutdown complete.")
