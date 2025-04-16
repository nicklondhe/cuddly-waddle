'''Main server'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app import DATA_DIR
from app.models.puzzle import PuzzleResponse
from scripts.puzzle_generator import PuzzleGenerator


app = FastAPI()
logger.info(f"Initializing puzzle generator with data directory: {DATA_DIR}")
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
    logger.info("Received request to generate a new puzzle")
    try:
        puzzle = await puzzlegen.get_new_puzzle()
        if puzzle:
            logger.info(f"Successfully generated puzzle with {len(puzzle)} categories")
            return PuzzleResponse.from_category_dict(puzzle)
        else:
            logger.error("Failed to generate puzzle: empty response from puzzle generator")
            return "Could not generate puzzle!"
    except Exception as e:
        logger.error(f"Error generating puzzle: {str(e)}")
        raise
