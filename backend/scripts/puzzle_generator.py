'''Generating a puzzle from data'''
from typing import List, Dict
from pathlib import Path
import random

from loguru import logger

from app.models.movies import MovieData
from app.services.puzzle_service import PuzzleService


class PuzzleGenerator:
    '''Class that generates a puzzle'''
    def __init__(self, data_directory: str):
        self.data_directory = Path(data_directory)
        self.movies = self._load_movies()
        self.puzzle_service = PuzzleService()

    def _load_movies(self) -> List[MovieData]:
        """Load all movie data from JSON files in the data directory."""
        movies = []
        for json_file in self.data_directory.glob("*.json"):
            if 'processed_pages' in json_file.name:
                continue
            movies.append(MovieData.from_json_file(json_file))

        logger.info(f'Loaded {len(movies)} movies')
        return movies

    def generate_candidate_set(self, size: int = 25) -> List[str]:
        """Generate a diverse subset of movies for puzzle creation."""
        logger.info("Generating candidates!")
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

            if movie.director and movie.director not in directors:
                score += 1
            for genre in movie.genres:
                if genre not in genres:
                    score += 0.5
            if movie.year:
                decade = (movie.year // 10) * 10
                if decade not in decades:
                    score += 1

            # Add movie if it adds sufficient diversity
            if score >= 1:
                selected.append(movie.format_for_prompt())
                if movie.director:
                    directors.add(movie.director)
                genres.update(movie.genres)
                if decade:
                    decades.add(decade)

        return selected

    def validate_grouping(self, grouping: Dict[str, List[str]], movies: List[Dict]) -> bool:
        """Validate that the grouping uses each movie exactly once and has 4 groups of 4."""
        logger.info("Validating groups!")
        # Convert movies to set of titles for easy lookup
        movie_titles = {movie['title'] for movie in movies}

        # Check we have exactly 4 groups
        if len(grouping) != 4:
            logger.error(f'Total groups = {len(grouping)}')
            return False

        # Keep track of used movies
        used_movies = set()

        # Check each group
        for group in grouping.values():
            # Each group should have exactly 4 movies
            if len(group) != 4:
                logger.error(f'Invalid group: {group}')
                return False

            # Each movie should exist in our dataset
            for movie in group:
                if movie not in movie_titles:
                    logger.error(f'Unknown movie: {movie}')
                    return False
                if movie in used_movies:
                    logger.error(f'Doubly used movie: {movie}')
                    return False
                used_movies.add(movie)

        # Check we used exactly 16 movies
        return len(used_movies) == 16

    async def get_new_puzzle(self) -> Dict:
        '''Generates a new puzzle'''
        candidates = self.generate_candidate_set(30)
        puzzle = await self.puzzle_service.generate_puzzle(candidates)
        return puzzle
