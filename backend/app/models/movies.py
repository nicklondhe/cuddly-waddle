'''All movies related data models'''
from pathlib import Path
from typing import List, Optional

import json

from pydantic import BaseModel, Field


class MovieData(BaseModel):
    '''Movie data model'''
    title: str = Field(description="The title of the movie")
    year: Optional[int] = Field(description="Release year of the movie")
    director: Optional[str] = Field(description="Name of the movie's director")
    main_cast: List[str] = Field(description="List of up to 5 main actors in the movie")
    music_director: Optional[str] = Field(description="Name of the music director")
    producer: Optional[str] = Field(description="Name of the movie's producer")
    genres: List[str] = Field(description="List of genres for the movie")
    plot_themes: List[str] = Field(description="3-4 major themes or elements from the plot")
    awards: List[str] = Field(description="Major awards won by the movie")

    @classmethod
    def from_json_file(cls, file_path: Path | str) -> 'MovieData':
        """Load and validate movies from a JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            movie_json = json.load(f)
            return cls.model_validate(movie_json)

    def format_for_prompt(self) -> str:
        """Format movie data for LLM prompt"""
        fields = [
            ("Title", self.title),
            ("Year", str(self.year)),
            ("Director", self.director or "Unknown"),
            ("Genres", ", ".join(self.genres)),
            ("Cast", ", ".join(self.main_cast)),
            ("Themes", ", ".join(self.plot_themes)),
            ("Awards", ", ".join(self.awards))
        ]
        return "\n".join(f"{field}: {value}" for field, value in fields)
