import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skillset import Skillset
from config.settings import OPENAI_API_KEY, EXA_API_KEY
from util.llm_model import llm_model
from exa_py import Exa
import textwrap
from datetime import datetime, timedelta
import logging
import asyncio
from pydantic import BaseModel, PrivateAttr
from typing import Optional, List, Dict, Any

class InternetSearch(Skillset, BaseModel):
    _exa: Optional[Exa] = PrivateAttr(default=None)
    _answer_num: int = PrivateAttr(default=5)
    _debug: bool = PrivateAttr(default=False)
    _logger: logging.Logger = PrivateAttr(default=None)

    def __init__(self, name: str = "Internet Search", description: str = "Perform internet searches and summarize results", debug: bool = False, answer_num: int = 5):
        super().__init__(name=name, description=description)
        self._exa = Exa(EXA_API_KEY)
        self._answer_num = answer_num
        self._debug = debug
        self._setup_logger()

    def _setup_logger(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG if self._debug else logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    @property
    def exa(self): return self._exa
    @property
    def answer_num(self): return self._answer_num
    @property
    def debug(self): return self._debug
    @property
    def logger(self): return self._logger

    async def generate_search_query(self, user_question: str) -> str:
        prompt = f"Generate a search query based on this question: {user_question}"
        return llm_model.get_response("G1", prompt).strip()

    def perform_search(self, search_query: str) -> Dict:
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        return self.exa.search_and_contents(search_query, use_autoprompt=True, start_published_date=one_week_ago)

    def extract_urls(self, search_response: Dict) -> List[str]:
        return [result.url for result in search_response.results]

    async def generate_summary(self, text: str) -> str:
        prompt = f"Briefly summarize the following content:\n\n{text}"
        return llm_model.get_response("G1", prompt).strip()

    async def exec_report(self, user_question: str, top_results: List[Dict]) -> str:
        article_summaries = [f"Title: {result['title']}\nSummary: {result['summary']}\n" for result in top_results]
        report_prompt = f"""
        Generate a brief status report (less than 200 words) for the following research query:
        "{user_question}"

        The search found {len(top_results)} articles. Summarize what they are about in 1 sentence each.

        Here are the article titles and summaries:
        """ + "\n".join(article_summaries)

        return llm_model.get_response("G1", report_prompt).strip()

    async def _arun(self, query: str) -> Dict[str, Any]:
        search_query = await self.generate_search_query(query)
        self.logger.debug(f"Search query: {search_query}")

        search_response = self.perform_search(search_query)
        urls = self.extract_urls(search_response)
        self.logger.debug("URLs:\n" + "\n".join(urls))

        results = search_response.results[:self.answer_num]
        self.logger.debug(f"Processing top {len(results)} results.")

        top_results = []
        for result_item in results:
            summary = await self.generate_summary(result_item.text)
            self.logger.debug(f"Summary for {result_item.url}:\n{result_item.title}\n{textwrap.fill(summary, 80)}")
            top_results.append({'title': result_item.title, 'summary': summary, 'url': result_item.url})

        exec_report = await self.exec_report(query, top_results)
        self.logger.debug(f"Executive Report:\n{exec_report}")

        return {
            "exec_report": exec_report,
            "top_results": top_results
        }

    def _run(self, query: str) -> Dict[str, Any]:
        return asyncio.run(self._arun(query))

# Example usage
if __name__ == "__main__":
    internet_search = InternetSearch(debug=True, answer_num=2)
    query = "What's the recent news about Telegram and TONCOIN?"
    result = internet_search.run(query)
    print("\nExecutive Report:")
    print(result["exec_report"])
    print("\nTop Results:")
    for item in result["top_results"]:
        print(f"- {item['title']}: {item['summary'][:100]}...")