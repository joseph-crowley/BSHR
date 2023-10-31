
#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os 
from pprint import pprint
import requests


# Add the project config to the Python path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import config.settings

'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = config.settings.BING_SEARCH_V7_SUBSCRIPTION_KEY
endpoint = config.settings.BING_SEARCH_V7_ENDPOINT + "/v7.0/search"

# Query term(s) to search for.
query = "Microsoft"

# Construct a request
mkt = 'en-US'
params = { 'q': query, 'mkt': mkt }
headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

# Call the API
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    response_json = response.json()

    # Extracting relevant information
    simplified_results = []
    for item in response_json.get('webPages', {}).get('value', []):
        simplified_result = {
            "extract": item.get('snippet', ''),
            "source": item.get('url', '')
        }
        simplified_results.append(simplified_result)

    # Output simplified results
    pprint(simplified_results)

except Exception as ex:
    raise ex
