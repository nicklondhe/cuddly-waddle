'''Download movie wikipedia pages'''
from typing import Dict, List

import json
import random
import time

import wikipediaapi

from loguru import logger

from app import DATA_DIR
from app.services.movie_service import MovieDataService


class BollywoodDataCollector:
    '''Data collector from wikipedia'''
    def __init__(self):
        '''Constructor'''
        self.wiki = wikipediaapi.Wikipedia(
            'CuddlyWaddle (nikhillo@buffalo.edu)',  # Replace with your email
            'en'
        )

        self.movie_service = MovieDataService()

        # Create data directory if it doesn't exist
        self.data_dir = DATA_DIR
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

    async def extract_movie_data(self, page_title: str) -> Dict:
        '''Extract movie data using langchain + wikipedia api'''
        try:
            page = self.wiki.page(page_title)
            if not page.exists():
                return None

            movie_data = await self.movie_service.extract_movie_data(page.text)

            return movie_data

        except Exception as e:
            logger.error(f"Error processing {page_title}: {str(e)}")
            return None

    async def collect_and_save(self, category_name: str, max_pages: int):
        '''Collect pages for the given category and save them to disk'''
        pages = self.get_category_members(category_name, max_pages)

        for page_title in pages:
            logger.info(f'Processing: {page_title}')

            movie_data = await self.extract_movie_data(page_title)
            if movie_data:
                # Save individual movie data
                output_file = self.data_dir / f"{page_title.replace('/', '_')}.json"
                output_file.write_text(json.dumps(movie_data, indent=2))

                # Mark as processed
                self.processed_pages.add(page_title)

            # Be nice to APIs
            time.sleep(2)

        self.save_processed_pages()
