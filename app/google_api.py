import os

import httpx


class GoogleSearch:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    def _search(self, query: str, **params):
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            **params,
        }
        response = httpx.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_search_results(self, query: str, count: int):
        if not (1 <= count <= 1000):
            raise Exception("Count must be between 1 and 1000")
        search_results = []
        for i in range(1, count + 1):
            response = self._search(query=query, start=i)
            search_results.extend(response.get("items", []))
        # print(search_results)
        return search_results
