"""
agents/argument_agent.py
------------------------
Generates additional targeted arguments, counter-arguments,
and cross-examination questions on demand.
(Can be called independently for deeper analysis.)
"""

from llm.groq_client import GroqClient


_ARG_SYSTEM = """You are an experienced Indian trial lawyer.
Generate sharp, legally grounded arguments for court proceedings.
Always cite specific IPC/CrPC/CPC sections when making legal points.
Be direct, persuasive, and thorough.
"""


class ArgumentAgent:
    """Generates targeted arguments and counter-arguments."""

    def __init__(self):
        self.llm = GroqClient(temperature=0.4)

    def generate_arguments(
        self,
        case_description: str,
        rag_context: str,
        side: str = "petitioner",
    ) -> str:
        """
        Parameters
        ----------
        case_description : raw case text
        rag_context      : formatted string of retrieved legal sections
        side             : "petitioner" or "respondent"

        Returns
        -------
        Detailed argument string
        """
        prompt = f"""
Case Description:
{case_description}

Relevant Legal Sections:
{rag_context}

Generate 5 strong legal arguments for the {side.upper()}.
For each argument:
1. State the argument clearly
2. Cite the specific legal section that supports it
3. Explain how the facts satisfy the legal requirements
4. Anticipate the counter-argument and rebut it
"""
        return self.llm.generate(
            system_prompt=_ARG_SYSTEM,
            user_prompt=prompt,
            max_tokens=2048,
        )

    def generate_cross_examination(
        self, case_description: str, witness_role: str = "prosecution witness"
    ) -> str:
        """Generate cross-examination questions for a specific witness."""
        prompt = f"""
Case Description:
{case_description}

Generate 7 sharp cross-examination questions to ask a {witness_role}.
Each question should:
- Be designed to reveal inconsistencies or weaknesses
- Follow proper cross-examination technique (leading questions)
- Target credibility, motive, or factual contradictions
"""
        return self.llm.generate(
            system_prompt=_ARG_SYSTEM,
            user_prompt=prompt,
            max_tokens=1024,
        )
