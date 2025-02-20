'''Main server'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import DATA_DIR
from app.models.puzzle import PuzzleResponse
from scripts.puzzle_generator import PuzzleGenerator


app = FastAPI()
puzzlegen = PuzzleGenerator(DATA_DIR)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/puzzle", response_model=PuzzleResponse)
async def generate_puzzle():
    '''Get a puzzle'''
    puzzle = await puzzlegen.get_new_puzzle()
    return PuzzleResponse.from_category_dict(puzzle) if puzzle else "Could not generate puzzle!"
