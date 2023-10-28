import re # Jetbrains Test
import requests
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from metaphor_python import Metaphor, SearchResponse
from metaphor_python import Metaphor
import predictor

import replicate
import os

def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])

def to_camel_case(data: dict) -> dict:
    return {snake_to_camel(k): v for k, v in data.items() if v is not None}

def camel_to_snake(camel_str: str) -> str:
    snake_str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", snake_str).lower()

def to_snake_case(data: dict) -> dict:
    return {camel_to_snake(k): v for k, v in data.items()}

SEARCH_OPTIONS_TYPES = {
    'query': str,  # Declarative suggestion for search.
    'num_results': int,  # Number of results (Default: 10, Max for basic: 30).
    'include_domains': list,  # Domains to search from; exclusive with 'exclude_domains'.
    'exclude_domains': list,  # Domains to omit; exclusive with 'include_domains'.
    'start_crawl_date': str,  # Results after this crawl date. ISO 8601 format.
    'end_crawl_date': str,  # Results before this crawl date. ISO 8601 format.
    'start_published_date': str,  # Results after this publish date; excludes links with no date. ISO 8601 format.
    'end_published_date': str,  # Results before this publish date; excludes links with no date. ISO 8601 format.
    'use_autoprompt': bool,  # Convert query to Metaphor (Higher latency, Default: false).
    'type': str,  # 'keyword' or 'neural' (Default: neural). Choose 'neural' for high-quality, semantically relevant content in popular domains. 'Keyword' is for specific, local, or obscure queries.
}

FIND_SIMILAR_OPTIONS_TYPES = {
    'url': str, # The url for which you would like to find similar links
    'num_results': int,
    'include_domains': list,
    'exclude_domains': list,
    'start_crawl_date': str,
    'end_crawl_date': str,
    'start_published_date': str,
    'end_published_date': str,
}

def validate_search_options(options: Dict[str, Optional[object]]) -> None:
    for key, value in options.items():
        if key not in SEARCH_OPTIONS_TYPES:
            raise ValueError(f"Invalid option: '{key}'")
        if not isinstance(value, SEARCH_OPTIONS_TYPES[key]):
            raise ValueError(f"Invalid type for option '{key}': Expected {SEARCH_OPTIONS_TYPES[key]}, got {type(value)}")
        if key in ['include_domains', 'exclude_domains'] and not value:
            raise ValueError(f"Invalid value for option '{key}': cannot be an empty list")

def validate_find_similar_options(options: Dict[str, Optional[object]]) -> None:
    for key, value in options.items():
        if key not in FIND_SIMILAR_OPTIONS_TYPES:
            raise ValueError(f"Invalid option: '{key}'")
        if not isinstance(value, FIND_SIMILAR_OPTIONS_TYPES[key]):
            raise ValueError(f"Invalid type for option '{key}': Expected {FIND_SIMILAR_OPTIONS_TYPES[key]}, got {type(value)}")
        if key in ['include_domains', 'exclude_domains'] and not value:
            raise ValueError(f"Invalid value for option '{key}': cannot be an empty list")

@dataclass
class Result:
    title: str
    url: str
    published_date: Optional[str] = None

    def __init__(self, title, url, published_date=None, **kwargs):
        self.title = title
        self.url = url
        self.published_date = published_date
    def __str__(self):
        return (f"Title: {self.title}\n"
                f"URL: {self.url}\n"
                f"Published Date: {self.published_date}\n")

@dataclass
class DocumentContent:
    id: str
    url: str
    title: str
    extract: str

    def __init__(self, id, url, title, extract, **kwargs):
        self.id = id
        self.url = url
        self.title = title
        self.extract = extract

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"URL: {self.url}\n"
                f"Title: {self.title}\n"
                f"Extract: {self.extract}")

@dataclass
class GetContentsResponse:
    contents: List[DocumentContent]

    def __str__(self):
        return "\n\n".join(str(content) for content in self.contents)

@dataclass
class SearchResponse:
    results: List[Result]
    autoprompt_string: Optional[str] = None
    api: Optional['Metaphor'] = field(default=None, init=False)

    def get_contents(self):
        if self.api is None:
            raise Exception("API client is not set. This method should be called on a SearchResponse returned by the 'search' method of 'Metaphor'.")
        ids = [result.id for result in self.results]
        return self.api.get_contents(ids)

    def __str__(self):
        output = "\n\n".join(str(result) for result in self.results)
        if self.autoprompt_string:
            output += f"\n\nAutoprompt String: {self.autoprompt_string}"
        return output

class Metaphor:
    def __init__(self, api_key: str, base_url: str = "https://api.metaphor.systems", user_agent: str = "metaphor-python 0.1.16"):
        self.base_url = base_url
        self.headers = {"x-api-key": api_key, "User-Agent": user_agent}

    def search(self, query: str, num_results: Optional[int] = None, include_domains: Optional[List[str]] = None,
               exclude_domains: Optional[List[str]] = None, start_crawl_date: Optional[str] = None,
               end_crawl_date: Optional[str] = None, start_published_date: Optional[str] = None,
               end_published_date: Optional[str] = None, use_autoprompt: Optional[bool] = None,
               type: Optional[str] = None) -> SearchResponse:
        options = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        validate_search_options(options)
        request = {'query': query}
        request.update(to_camel_case(options))
        response = requests.post(f"{self.base_url}/search", json=request, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}. Message: {response.text}")
        results = [Result(**to_snake_case(result)) for result in response.json()["results"]]
        autoprompt_string = response.json()["autopromptString"] if "autopromptString" in response.json() else None
        search_response = SearchResponse(results=results, autoprompt_string=autoprompt_string)
        search_response.api = self
        return search_response

    def find_similar(self, url: str, num_results: Optional[int] = None, include_domains: Optional[List[str]] = None,
                     exclude_domains: Optional[List[str]] = None, start_crawl_date: Optional[str] = None,
                     end_crawl_date: Optional[str] = None, start_published_date: Optional[str] = None,
                     end_published_date: Optional[str] = None) -> SearchResponse:
        options = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        validate_find_similar_options(options)
        request = {'url': url}
        request.update(to_camel_case(options))
        response = requests.post(f"{self.base_url}/findSimilar", json=request, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}. Message: {response.text}")
        results = [Result(**to_snake_case(result)) for result in response.json()["results"]]
        find_similar_response = SearchResponse(results=results)
        find_similar_response.api = self
        return find_similar_response

    def get_contents(self, ids: List[str]) -> GetContentsResponse:
        if len(ids) == 0:
            raise ValueError("ids cannot be empty")
        response = requests.get(f"{self.base_url}/contents", params=to_camel_case({"ids": ids}), headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}. Message: {response.text}")
        return GetContentsResponse([DocumentContent(**to_snake_case(document)) for document in response.json()["contents"]])
    
api_key = "8fb2527a-168c-4a96-bc40-bcd2e02f60e6"
metaphor_api = Metaphor(api_key)

metaphor = Metaphor("8fb2527a-168c-4a96-bc40-bcd2e02f60e6")

os.environ["REPLICATE_API_TOKEN"] = "r8_5uSxtmgLLmbIzXmF5UtUyqiSugYzk5C09RUnU"

#REPLICATE_API_TOKEN="r8_eiTO762GR8NKbmPt9AwPZnqsfh5keny2zSiNe"
# Define your prompt
disease_class = "psoriasis"
prompt = "Provide an friendly, accommodating, understandable explanation of " + disease_class + "No need to give description of what you do"

replicate.Client(api_token= "r8_5uSxtmgLLmbIzXmF5UtUyqiSugYzk5C09RUnU")
output = replicate.run(
    "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
    input={"prompt": prompt}
)
# The meta/llama-2-70b-chat model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.

Result = ""
for item in output:
    Result = Result + item
    # print(item, end = '')
print(Result)

from metaphor_python import Metaphor
metaphor = Metaphor("8fb2527a-168c-4a96-bc40-bcd2e02f60e6")

disease_class = "psoriasis"
results = metaphor.search('more information about ' + disease_class, use_autoprompt=True)
#print(results)

query = "more information about " + disease_class
metaphor = Metaphor(api_key=api_key)

def extract_info():
  search_response = metaphor.search(query=query, type="neural")

  mapped_results = []
  for result in search_response.results:
      mapped_result = {
          "title": result.title,
          "url": result.url,
          "published_date": result.published_date
        }
      mapped_results.append(mapped_result)
      return mapped_results

outputs = extract_info()

for output in outputs:
  print(output)