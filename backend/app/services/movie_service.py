'''A movie data extraction service'''
from langchain.output_parsers.json import SimpleJsonOutputParser

from app.models.movies import MovieData
from app.services.base import BaseLLMService


class MovieDataService(BaseLLMService):
    '''Service impl'''
    def __init__(self):
        super().__init__()
        self.parser = None
        self.chain = None
        self._setup_chain()

    def _setup_chain(self):
        '''Setup chain'''
        self.parser = SimpleJsonOutputParser(pydantic_object=MovieData)
        prompt_template = """
            Extract structured movie data from the following Wikipedia content and return it as JSON.
            Do not include any introductory text, explanations, or markdown formatting - return ONLY the JSON object.

            {format_instructions}

            Content: {content}

            Remember: Return the JSON object only, with no additional text before or after."""
        self.chain = self._create_chain(prompt_template=prompt_template,
                                        parser=self.parser, input_variables=["content"])

    async def extract_movie_data(self, content: str) -> MovieData:
        """Extract structured data from movie content"""
        result = await self.chain.ainvoke({"content": content})
        return result
