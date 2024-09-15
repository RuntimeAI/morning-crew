import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skillset import Skillset
from config.settings import OPENAI_API_KEY
from util.llm_model import llm_model
import logging
import asyncio
import markdown
from pydantic import BaseModel, PrivateAttr
from typing import Optional, List, Dict, Any
from weasyprint import HTML

class MeetingNotesDraft(Skillset, BaseModel):
    _debug: bool = PrivateAttr(default=False)
    _logger: logging.Logger = PrivateAttr(default=None)

    def __init__(self, name: str = "Meeting Notes Draft", description: str = "Generate meeting notes from conversation records and cached contents", debug: bool = False):
        super().__init__(name=name, description=description)
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
    def debug(self): return self._debug
    @property
    def logger(self): return self._logger

    async def generate_meeting_notes(self, conversation_records: List[Dict[str, str]], cached_contents: List[str]) -> Dict[str, str]:
        prompt = f"""
        Generate a meeting notes draft based on the following conversation records and cached contents using the provided template. Generate three versions: Markdown, HTML, and PDF.

        Template:
        # Daily Internal Financial Meeting Notes

        **Date:** [Insert Date]  
        **Time:** [Insert Time]  
        **Location:** [Virtual/Conference Room]

        ---

        ## Attendees:
        - **[CEO Name]**
        - **Taylor Mason** – Financial Researcher
        - **Ben Kim** – Analyst Intern
        - **Dollar Bill** – Senior Trader

        ---

        ## Agenda Overview:
        1. Discussion of Trading Opportunities
        2. Industrial News & Market Signals
        3. Risk Assessment and Mitigation Strategies
        4. Action Plan

        ---

        ### Meeting Notes:

        #### 1. Trading Opportunities:
        - **Discussed Opportunities:**
          - [Insert specific trading opportunities discussed]
          - Key insights from Taylor Mason: [Summarize insights from Taylor on market trends, sentiment analysis, etc.]
          - Dollar Bill's perspective on trades: [Summarize Dollar Bill's views or trade recommendations]

        - **Potential Assets/Markets:**
          - [Insert assets or markets under consideration for trading]
          
        - **Relevant Links/Resources:**
          - [Include any links or resources mentioned, such as reports or charts]

        ---

        #### 2. Industrial News & Market Signals:
        - **Key Market News:**
          - [Insert important industrial news or economic indicators discussed]
          - Source: [Insert links or references to the news articles or data]
          
        - **Market Signals Identified:**
          - [Summarize signals observed by Taylor or the team]
          - How it could impact trading strategy: [Insert team discussion]

        ---

        #### 3. Risk Assessment:
        - **Potential Risks:**
          - [Insert any risks identified during the discussion]
          
        - **Mitigation Strategies:**
          - [Include strategies proposed by the team, e.g., hedging, position sizing]

        ---

        #### 4. Action Plan:
        - **Tasks Assigned:**
          - **Taylor Mason**: [Insert task, e.g., further research on market trends]
          - **Ben Kim**: [Insert task, e.g., consolidating meeting notes and drafting a report]
          - **Dollar Bill**: [Insert task, e.g., preparing trade execution plan]
          
        - **Follow-Up Items:**
          - [Insert any follow-up items or deadlines]

        ---

        ### Additional Notes:
        - [Insert any miscellaneous points or observations]
          
        ---

        **Next Meeting Date:** [Insert date and time of the next meeting]  
        **Prepared by:** Ben Kim – Analyst Intern

        Conversation Records:
        {conversation_records}

        Cached Contents:
        {cached_contents}
        """
        response = llm_model.get_response("G1", prompt).strip()
        return {
            "markdown": response,
            "html": self.convert_to_html(response),
            "pdf": self.convert_to_pdf(response)
        }

    def convert_to_html(self, markdown_text: str) -> str:
        # Convert markdown to HTML
        return markdown.markdown(markdown_text)

    def convert_to_pdf(self, markdown_text: str) -> bytes:
        # Convert markdown to PDF
        html_text = markdown(markdown_text)
        pdf = HTML(string=html_text).write_pdf()
        return pdf

    async def _arun(self, conversation_records: List[Dict[str, str]], cached_contents: List[str]) -> Dict[str, Any]:
        meeting_notes = await self.generate_meeting_notes(conversation_records, cached_contents)
        self.logger.debug(f"Meeting Notes Draft:\n{meeting_notes}")

        return {
            "meeting_notes": meeting_notes
        }

    def _run(self, conversation_records: List[Dict[str, str]], cached_contents: List[str]) -> Dict[str, Any]:
        return asyncio.run(self._arun(conversation_records, cached_contents))

# Example usage
if __name__ == "__main__":
    meeting_notes_draft = MeetingNotesDraft(debug=True)
    conversation_records = [
        {"role": "user", "content": "Discuss the quarterly financial results."},
        {"role": "ai", "content": "The quarterly financial results show a 10% increase in revenue."}
    ]
    cached_contents = ["Quarterly financial report", "Revenue increased by 10%"]
    result = meeting_notes_draft._run(conversation_records, cached_contents)  # Use _run instead of run
    print("\nMeeting Notes Draft (Markdown):")
    print(result["meeting_notes"]["markdown"])
    print("\nMeeting Notes Draft (HTML):")
    print(result["meeting_notes"]["html"])
    # Save PDF to file
    with open("meeting_notes.pdf", "wb") as f:
        f.write(result["meeting_notes"]["pdf"])