'''A puzzle generation service'''
from langchain.output_parsers.json import SimpleJsonOutputParser

from app.services.base import BaseLLMService


class PuzzleService(BaseLLMService):
    '''Service impl'''
    def __init__(self):
        super().__init__()
        self.parser = None
        self.chain = None
        self._setup_chain()

    def _setup_chain(self):
        self.parser = SimpleJsonOutputParser()
        prompt_template = """
            Given these Bollywood movies, create a puzzle similar to NYT Connections where
            movies need to be grouped into 4 categories of 4 movies each.
            Each category should have a clear, specific connection (e.g., same director, similar themes, awards, decade of release, etc.).

            Please format your response as a JSON object where each key is the category name/connection,
            and the value is a list of 4 movie titles that belong to that category. 

            IMPORTANT: Make sure that each movie is used EXACTLY once and that each category has four films

            Make sure that the response is always a proper JSON object, ignore any movies that do not fit the request etc.
            Do not include any introductory text, explanations, or markdown formatting - return ONLY the JSON object.

            Return an empty object if unable to generate connections as requested

            Movies:
            {movies}
        """
        self.chain = self._create_chain(
            prompt_template=prompt_template,
            parser=self.parser,
            input_variables=["movies"]
        )

    async def generate_puzzle(self, movies_data: list[str]) -> dict:
        """Generate puzzle groups from movie data"""
        formatted_movies = "\n---\n".join(movies_data)
        return await self.chain.ainvoke({"movies": formatted_movies})
