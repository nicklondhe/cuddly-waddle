# Cuddly Waddle

A Bollywood-themed connections game inspired by NYT Connections. Group Bollywood movies, actors, directors, and themes into meaningful categories!

## Setup

### Backend
```bash
cd backend
conda env create -f environment.yml
conda activate cuddly-waddle
uvicorn app.main:app --reload