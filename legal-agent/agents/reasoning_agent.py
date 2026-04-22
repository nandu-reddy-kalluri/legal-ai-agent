"""
agents/reasoning_agent.py
-------------------------
Takes parsed case info + retrieved RAG docs and
produces the full 11-section legal analysis via Groq.
"""

from llm.groq_client       import GroqClient
from llm.prompt_templates  import build_legal_analysis_prompt


class ReasoningAgent:
    """Generates the structured 11-section legal analysis."""

    def __init__(self):
        self.llm = GroqClient(temperature=0.3)

    def analyze(self, case_description: str, rag_docs: list) -> str:
        """
        Parameters
        ----------
        case_description : raw case text
        rag_docs         : list of doc dicts from vector_store.search()

        Returns
        -------
        Full 11-section Markdown report as a string
        """
        system_prompt, user_prompt = build_legal_analysis_prompt(
            case_description, rag_docs
        )
        return self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=4096,
        )
