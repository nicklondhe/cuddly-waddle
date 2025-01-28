'''Download movie wikipedia pages'''
from pathlib import Path
from typing import Dict, List, Optional

import json
import os
import random
import time

from dotenv import load_dotenv
from langchain_anthropic.chat_models import ChatAnthropic
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

import wikipediaapi


load_dotenv()

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

class BollywoodDataCollector:
    '''Data collector from wikipedia'''
    def __init__(self):
        '''Constructor'''
        self.wiki = wikipediaapi.Wikipedia(
            'CuddlyWaddle (nikhillo@buffalo.edu)',  # Replace with your email
            'en'
        )
        self.llm = ChatAnthropic(
            model="claude-3-opus-latest",
            anthropic_api_key=os.getenv('CLAUDE_API_KEY'),
            temperature=0.2
        )

        self.parser = SimpleJsonOutputParser(pydantic_object=MovieData)

        prompt = PromptTemplate(
            template="""Extract structured movie data from the following Wikipedia content.
            
            {format_instructions}
            
            Content: {content}
            
            Return only the requested JSON structure.""",
            input_variables=["content"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        self.chain = prompt | self.llm | self.parser

        # Create data directory if it doesn't exist
        self.data_dir = Path("../data")
        self.data_dir.mkdir(exist_ok=True)

        # Keep track of processed pages
        self.processed_file = self.data_dir / "processed_pages.json"
        self.processed_pages = self.load_processed_pages()

    def load_processed_pages(self) -> set:
        '''Load processed pages'''
        if self.processed_file.exists():
            return set(json.loads(self.processed_file.read_text()))
        return set()

    def save_processed_pages(self):
        '''Save processed pages'''
        self.processed_file.write_text(json.dumps(list(self.processed_pages)))

    def get_category_members(self, category_name: str, max_pages: int) -> List[str]:
        '''Get list of pages not read so far and up to max pages under the given category'''
        category = self.wiki.page(f'Category:{category_name}')

        if not category.exists():
            raise ValueError(f'The category {category_name} does not exist')

        # shuffle
        members = list(category.categorymembers.values())
        random.shuffle(members)

        pages = []
        for member in members:
            #skip if category or already seen
            if member.namespace != wikipediaapi.Namespace.MAIN or \
                member.title in self.processed_pages:
                continue

            pages.append(member.title)

            if len(pages) >= max_pages:
                break
        return pages[:max_pages]

    def extract_movie_data(self, page_title: str) -> Dict:
        '''Extract movie data using langchain + wikipedia api'''
        try:
            page = self.wiki.page(page_title)
            if not page.exists():
                return None

            movie_data = self.chain.invoke({"content": page.text})
            return movie_data

        except Exception as e:
            print(f"Error processing {page_title}: {str(e)}")
            return None

    def collect_and_save(self, category_name: str, max_pages: int):
        '''Collect pages for the given category and save them to disk'''
        pages = self.get_category_members(category_name, max_pages)

        for page_title in pages:
            print (f'Processing: {page_title}')

            movie_data = self.extract_movie_data(page_title)
            if movie_data:
                # Save individual movie data
                output_file = self.data_dir / f"{page_title.replace('/', '_')}.json"
                output_file.write_text(json.dumps(movie_data, indent=2))

                # Mark as processed
                self.processed_pages.add(page_title)

            # Be nice to APIs
            time.sleep(2)

        self.save_processed_pages()
