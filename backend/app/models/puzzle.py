'''All puzzle related data models'''
from typing import List
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
        items = []
        groups = []
        
        # Create groups and items
        for group_id, (theme, movies) in enumerate(category_dict.items(), 1):
            # Add group
            groups.append(PuzzleGroup(id=group_id, theme=theme))
            
            # Add items for this group
            for movie in movies:
                items.append(PuzzleItem(
                    id=f"{group_id}-{movie}",
                    text=movie,
                    group_id=group_id
                ))
        
        # Shuffle items (optional, you can remove if you want to shuffle elsewhere)
        import random
        random.shuffle(items)
        
        return cls(items=items, groups=groups)
