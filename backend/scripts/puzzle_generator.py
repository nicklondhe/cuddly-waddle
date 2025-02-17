'''Generating a puzzle from data'''
from typing import List, Dict
from pathlib import Path
import json
import os
import random

from dotenv import load_dotenv
from langchain_anthropic.chat_models import ChatAnthropic
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import PromptTemplate


load_dotenv()


class PuzzleGenerator:
    '''Class that generates a puzzle'''
    def __init__(self, data_directory: str):
        self.data_directory = Path(data_directory)
        self.movies = self._load_movies()

    def _load_movies(self) -> List[Dict]:
        """Load all movie data from JSON files in the data directory."""
        movies = []
        for json_file in self.data_directory.glob("*.json"):
            if json_file == 'processed_pages.json':
                continue

            with open(json_file, 'r', encoding='utf-8') as f:
                movies.append(json.load(f))
        print (f'Loaded {len(movies)} movies')
        return movies

    def generate_candidate_set(self, size: int = 25) -> List[Dict]:
        """Generate a diverse subset of movies for puzzle creation."""
        print("Generating candidates!")
        if size > len(self.movies):
            return self.movies

        # Strategy: Select movies that have good variety in attributes
        selected = []
        directors = set()
        genres = set()
        decades = set()

        # Shuffle movies to randomize selection
        candidates = self.movies.copy()
        random.shuffle(candidates)

        for movie in candidates:
            # Skip if we already have enough movies
            if len(selected) >= size:
                break

            # Calculate diversity score based on new information this movie would add
            score = 0
            decade = None

            if movie['director'] and movie['director'] not in directors:
                score += 1
            for genre in movie['genres']:
                if genre not in genres:
                    score += 0.5
            if movie['year']:
                decade = (movie['year'] // 10) * 10
                if decade not in decades:
                    score += 1

            # Add movie if it adds sufficient diversity
            if score >= 1:
                selected.append(movie)
                if movie['director']:
                    directors.add(movie['director'])
                genres.update(movie['genres'])
                if decade:
                    decades.add(decade)

        return selected

    def generate_prompt(self, movies: List[Dict]) -> str:
        """Generate a prompt for Claude to create groupings."""
        print ("Generating prompt!")
        movies_data = []
        for movie in movies:
            movie_info = (
                f"Title: {movie['title']}\n"
                f"Year: {movie['year']}\n"
                f"Director: {movie['director']}\n"
                f"Genres: {', '.join(movie['genres'])}\n"
                f"Cast: {', '.join(movie['main_cast'])}\n"
                f"Themes: {', '.join(movie['plot_themes'])}\n"
                f"Awards: {', '.join(movie['awards'])}\n"
            )
            movies_data.append(movie_info)

        prompt = """
        Given these Bollywood movies, create a puzzle similar to NYT Connections where 
        movies need to be grouped into 4 categories of 4 movies each.
        Each category should have a clear, specific connection (e.g., same director, similar themes, awards, decade of release, etc.).

        Please format your response as a JSON object where each key is the category name/connection,
        and the value is a list of 4 movie titles that belong to that category. Make sure each movie is used exactly once.

        Make sure that the response is always a proper JSON object, ignore any movies that do not fit the request etc.

        Movies:
        """
        prompt += "\n---\n".join(movies_data)

        return prompt

    def validate_grouping(self, grouping: Dict[str, List[str]], movies: List[Dict]) -> bool:
        """Validate that the grouping uses each movie exactly once and has 4 groups of 4."""
        print ("Validating groups!")
        # Convert movies to set of titles for easy lookup
        movie_titles = {movie['title'] for movie in movies}

        # Check we have exactly 4 groups
        if len(grouping) != 4:
            print (f'Total groups = {len(grouping)}')
            return False

        # Keep track of used movies
        used_movies = set()

        # Check each group
        for group in grouping.values():
            # Each group should have exactly 4 movies
            if len(group) != 4:
                print (f'Invalid group: {group}')
                return False

            # Each movie should exist in our dataset
            for movie in group:
                if movie not in movie_titles:
                    print (f'Unknown movie: {movie}')
                    return False
                if movie in used_movies:
                    print (f'Doubly used movie: {movie}')
                    return False
                used_movies.add(movie)

        # Check we used exactly 16 movies
        return len(used_movies) == 16
    
    def get_new_puzzle(self) -> Dict:
        '''Generates a new puzzle'''
        candidates = self.generate_candidate_set(30)
        prompt = self.generate_prompt(candidates)
        return get_puzzle(prompt)

def get_puzzle(prompt_str: str) -> Dict:
    '''Generate puzzle using claude'''
    print ("Generating puzzle!")
    llm = ChatAnthropic(model='claude-3-opus-latest',
                        anthropic_api_key = os.getenv('CLAUDE_API_KEY'),
                        temperature=0.2) # what does temperature do?
    prompt = PromptTemplate(template=prompt_str)
    parser = SimpleJsonOutputParser() #TODO: parse errors
    chain = prompt | llm | parser
    output = chain.invoke({})
    return json.loads(output) if isinstance(output, str) else output

def main():
    '''Entrypoint method'''
    # Example usage
    generator = PuzzleGenerator("../data")

    # Generate candidate set
    candidates = generator.generate_candidate_set(30)

    # Generate prompt
    prompt = generator.generate_prompt(candidates)

    puzzle = get_puzzle(prompt)

    print(f'Puzzle: {puzzle}')

    # Validate
    is_valid = generator.validate_grouping(puzzle, candidates)
    print(f"\nGrouping validation result: {is_valid}")

if __name__ == "__main__":
    main()
