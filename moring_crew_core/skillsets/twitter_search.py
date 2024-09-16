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

class TwitterSearch(Skillset, BaseModel):
    _exa: Optional[Exa] = PrivateAttr(default=None)
    _tweet_num: int = PrivateAttr(default=5)
    _debug: bool = PrivateAttr(default=False)
    _logger: logging.Logger = PrivateAttr(default=None)

    def __init__(self, name: str = "Twitter Search", description: str = "Search Twitter and summarize results", debug: bool = False, tweet_num: int = 5):
        super().__init__(name=name, description=description)
        self._exa = Exa(EXA_API_KEY)
        self._tweet_num = tweet_num
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
    def tweet_num(self): return self._tweet_num
    @property
    def debug(self): return self._debug
    @property
    def logger(self): return self._logger

    async def generate_search_query(self, user_question: str) -> str:
        prompt = f"Generate a Twitter search query based on this question: {user_question}"
        return llm_model.get_response("G1", prompt).strip()

    def perform_twitter_search(self, search_query: str) -> Dict:
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        return self.exa.search_twitter_posts(
            search_query,
            start_published_date=one_week_ago,
            num_results=self.tweet_num
        )

    async def exec_twitter_report(self, user_question: str, tweets: List[Dict]) -> str:
        tweet_summaries = [f"Tweet by {tweet['author']}: {tweet['text'][:100]}..." for tweet in tweets]
        report_prompt = f"""
        Generate a brief status report (less than 200 words) for the following Twitter search query:
        "{user_question}"

        The search found {len(tweets)} tweets. Summarize the key points and general sentiment.

        Here are snippets from the tweets:
        """ + "\n".join(tweet_summaries)

        return llm_model.get_response("G1", report_prompt).strip()

    async def _arun(self, query: str) -> Dict[str, Any]:
        search_query = await self.generate_search_query(query)
        self.logger.debug(f"Search query: {search_query}")

        twitter_response = self.perform_twitter_search(search_query)
        tweets = self.extract_tweets(twitter_response)

        self.logger.debug(f"Found {len(tweets)} tweets")

        exec_report = await self.exec_twitter_report(query, tweets)
        self.logger.debug(f"Executive Report:\n{exec_report}")

        return {
            "exec_report": exec_report,
            "top_results": tweets[:self.tweet_num]
        }

    def _run(self, query: str) -> Dict[str, Any]:
        return asyncio.run(self._arun(query))

# Example usage
if __name__ == "__main__":
    twitter_search = TwitterSearch(debug=True, tweet_num=5)
    query = "What's the recent discussion about AI on Twitter?"
    result = twitter_search.run(query)
    print("\nExecutive Report:")
    print(result["exec_report"])
    print("\nTop Tweets:")
    for tweet in result["top_results"]:
        print(f"- {tweet['author']}: {tweet['text'][:100]}...")