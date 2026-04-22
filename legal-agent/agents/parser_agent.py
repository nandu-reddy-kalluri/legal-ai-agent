"""
agents/parser_agent.py
----------------------
Parses the raw case description and extracts:
- case type (criminal / civil / constitutional)
- key entities (parties, locations, amounts)
- refined search queries for RAG retrieval
"""

from llm.groq_client import GroqClient


_PARSER_SYSTEM = """You are a legal case parser. Given a case description, extract:
1. The likely type of case (Criminal/Civil/Constitutional)
2. Key parties (Petitioner, Respondent, Witnesses)
3. 3-5 precise search queries to retrieve relevant law sections from a RAG system
4. The primary legal concern in one sentence

Respond in this EXACT format:
CASE_TYPE: [Criminal/Civil/Constitutional/Mixed]
PETITIONER: [name or description]
RESPONDENT: [name or description]
PRIMARY_ISSUE: [one sentence]
SEARCH_QUERIES:
- [query 1]
- [query 2]
- [query 3]
- [query 4]
- [query 5]
"""


class ParserAgent:
    """Extracts structured information from a raw case description."""

    def __init__(self):
        self.llm = GroqClient(temperature=0.1)

    def parse(self, case_description: str) -> dict:
        """
        Returns a dict with:
            case_type, petitioner, respondent, primary_issue, search_queries
        """
        raw = self.llm.generate(
            system_prompt=_PARSER_SYSTEM,
            user_prompt=f"Case Description:\n{case_description}",
            max_tokens=512,
        )
        return self._parse_output(raw, case_description)

    def _parse_output(self, raw: str, fallback: str) -> dict:
        result = {
            "case_type":      "Criminal",
            "petitioner":     "Petitioner",
            "respondent":     "Respondent",
            "primary_issue":  fallback[:120],
            "search_queries": [fallback],
        }
        try:
            lines   = raw.strip().split("\n")
            queries = []
            in_q    = False
            for line in lines:
                line = line.strip()
                if line.startswith("CASE_TYPE:"):
                    result["case_type"] = line.split(":", 1)[1].strip()
                elif line.startswith("PETITIONER:"):
                    result["petitioner"] = line.split(":", 1)[1].strip()
                elif line.startswith("RESPONDENT:"):
                    result["respondent"] = line.split(":", 1)[1].strip()
                elif line.startswith("PRIMARY_ISSUE:"):
                    result["primary_issue"] = line.split(":", 1)[1].strip()
                elif line.startswith("SEARCH_QUERIES:"):
                    in_q = True
                elif in_q and line.startswith("-"):
                    q = line.lstrip("- ").strip()
                    if q:
                        queries.append(q)
            if queries:
                result["search_queries"] = queries
        except Exception:
            pass
        return result
