'''Base LLM service'''
from typing import Any

import os

from dotenv import load_dotenv
from langchain_anthropic.chat_models import ChatAnthropic

from langchain.prompts import PromptTemplate

load_dotenv()

class BaseLLMService:
    """Base class for LLM services using LangChain and Claude"""

    def __init__(self, model_name: str = "claude-3-opus-latest"):
        self.llm = ChatAnthropic(
            model=model_name,
            anthropic_api_key=os.getenv('CLAUDE_API_KEY'),
            temperature=0.2
        )
        self._setup_chain()

    def _setup_chain(self):
        """Override this in child classes to set up specific prompt and parser"""
        raise NotImplementedError

    def _create_chain(self, prompt_template: str, parser: Any, input_variables: list[str]):
        """Creates a LangChain chain with the given prompt and parser"""
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_variables,
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        return prompt | self.llm | parser
