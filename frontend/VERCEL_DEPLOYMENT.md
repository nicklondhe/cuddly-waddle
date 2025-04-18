# Vercel Deployment Guide

This document explains how to deploy the Bollywood Rishtey game to Vercel without requiring a backend.

## Deployment Architecture

For Vercel deployment, we pre-generate static puzzle files locally and include them in the repository, instead of relying on a dynamic backend API. This approach:

1. Eliminates the need for a separate backend deployment
2. Reduces hosting costs
3. Improves reliability and performance

## How It Works

1. **Static Puzzle Generation (Local Process)**:
   - Run your local development backend
   - Execute the puzzle generator script (`npm run generate-puzzles`)
   - The script generates a specified number of puzzles (default: 20)
   - Puzzles are saved as JSON files in the `/public/puzzles/` directory
   - An index file is created with references to all puzzles

2. **Runtime Puzzle Selection**:
   - When a user visits the app, the frontend loads the puzzle index file
   - Randomly selects a puzzle from the available options
   - Fetches and displays the puzzle data

3. **Fallback Mechanism**:
   - If static puzzles cannot be loaded, the app falls back to a sample puzzle included in the codebase

## Deployment Steps

1. **Before Deploying to Vercel**:
   
   a. Pre-generate the puzzles locally:
   ```bash
   # Start your backend first
   cd backend/app && uvicorn main:app --reload
   
   # In another terminal, generate puzzles
   cd frontend
   npm install
   npm run generate-puzzles
   
   # Verify puzzles were created
   ls -la public/puzzles/
   ```
   
   b. Commit the generated puzzles to your repository:
   ```bash
   git add public/puzzles/
   git commit -m "Add pre-generated puzzles for Vercel deployment"
   git push
   ```

2. **Deploy to Vercel**:
   - Connect your GitHub repository to Vercel
   - Set the root directory to `/frontend`
   - Vercel will automatically use the configuration in `vercel.json`
   - The build process will build the app using your pre-generated puzzles

## Managing Puzzles

- **Adding More Puzzles**: 
  - Run your local backend
  - Run `npm run generate-puzzles` again 
  - Commit and push the new puzzles
  - Redeploy to Vercel or trigger a new deployment

- **Customizing Number of Puzzles**: 
  - Change the `NUM_PUZZLES` constant in `scripts/generate_static_puzzles.js`
  - Run the generator again

## Alternative Approach: Deploy Backend

If you prefer having dynamically generated puzzles and don't mind maintaining a backend:

1. Deploy your backend to a service like Render, Fly.io, Railway, or Heroku
2. Update your frontend's `.env.production` to point to your deployed backend URL
3. Use the API version of puzzle loading in production

## Troubleshooting

- **Error: Missing puzzles**: Check that the puzzle directories and files were committed to your repository.
- **Limited Puzzle Variety**: To increase variety, generate more puzzles locally and push them to your repository.
- **Game Not Loading**: Check the browser console for errors related to puzzle loading.

## Future Improvements

- Create a GitHub Action to automatically generate new puzzles periodically
- Implement caching and persistence mechanisms to track which puzzles a user has already played
- Add puzzle difficulty ratings and allow users to select difficulty level