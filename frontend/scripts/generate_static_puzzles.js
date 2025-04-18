/**
 * Script to generate static puzzles for Vercel deployment
 * Fetches puzzles from the local backend API and saves them as JSON files
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import fetch from 'node-fetch';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const BACKEND_URL = 'http://localhost:8000';
const OUTPUT_DIR = path.join(__dirname, '../public/puzzles');
const NUM_PUZZLES = 20; // Number of puzzles to generate

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  console.log(`Created directory: ${OUTPUT_DIR}`);
}

async function fetchPuzzle() {
  try {
    const response = await fetch(`${BACKEND_URL}/puzzle`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch puzzle: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching puzzle:', error);
    throw error;
  }
}

async function generatePuzzles() {
  console.log(`Generating ${NUM_PUZZLES} static puzzles...`);
  
  for (let i = 0; i < NUM_PUZZLES; i++) {
    try {
      const puzzle = await fetchPuzzle();
      const filePath = path.join(OUTPUT_DIR, `puzzle_${i+1}.json`);
      
      fs.writeFileSync(filePath, JSON.stringify(puzzle, null, 2));
      console.log(`Generated puzzle ${i+1}/${NUM_PUZZLES}`);
      
      // Add a small delay to avoid overwhelming the backend
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error(`Failed to generate puzzle ${i+1}:`, error);
    }
  }
  
  // Generate an index file that lists all available puzzles
  const puzzleIndex = {
    puzzles: Array.from({ length: NUM_PUZZLES }, (_, i) => ({
      id: i + 1,
      path: `/puzzles/puzzle_${i + 1}.json`
    }))
  };
  
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'index.json'), 
    JSON.stringify(puzzleIndex, null, 2)
  );
  
  console.log(`Generated index file with ${NUM_PUZZLES} puzzles`);
}

generatePuzzles().catch(console.error);