'''All puzzle related data models'''
from typing import List
from loguru import logger
from pydantic import BaseModel


class PuzzleItem(BaseModel):
    '''A puzzle item'''
    id: str
    text: str
    group_id: int

class PuzzleGroup(BaseModel):
    '''A puzzle group'''
    id: int
    theme: str

class PuzzleResponse(BaseModel):
    '''A puzzle response as items and groups'''
    items: List[PuzzleItem]
    groups: List[PuzzleGroup]

    @classmethod
    def from_category_dict(cls, category_dict: dict):
        '''Convert puzzle dict to PuzzleResponse'''
        try:
            logger.info(f"Converting category dictionary with {len(category_dict)} categories")
            items = []
            groups = []

            # Create groups and items
            for group_id, (theme, movies) in enumerate(category_dict.items(), 1):
                logger.debug(f"Processing group {group_id}: {theme} with {len(movies)} movies")

                # Add group
                groups.append(PuzzleGroup(id=group_id, theme=theme))

                # Add items for this group
                for movie in movies:
                    items.append(PuzzleItem(
                        id=f"{group_id}-{movie}",
                        text=movie,
                        group_id=group_id
                    ))

            logger.info(f"Created PuzzleResponse with {len(groups)} groups and {len(items)} items")
            return cls(items=items, groups=groups)
        except Exception as e:
            logger.error(f"Error converting puzzle dictionary to response: {str(e)}")
            raise
