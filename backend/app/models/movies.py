'''All movies related data models'''
from typing import List, Optional

from pydantic import BaseModel, Field


class MovieData(BaseModel):
    '''Movie data model'''
    title: str = Field(description="The title of the movie")
    year: int = Field(description="Release year of the movie")
    director: Optional[str] = Field(description="Name of the movie's director")
    main_cast: List[str] = Field(description="List of up to 5 main actors in the movie")
    music_director: Optional[str] = Field(description="Name of the music director")
    producer: Optional[str] = Field(description="Name of the movie's producer")
    genres: List[str] = Field(description="List of genres for the movie")
    plot_themes: List[str] = Field(description="3-4 major themes or elements from the plot")
    awards: List[str] = Field(description="Major awards won by the movie")
