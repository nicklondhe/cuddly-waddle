# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- **Frontend**: `npm run dev` (development), `npm run build` (production), `npm run preview` (preview build)
- **Backend**: `cd backend && conda env create -f environment.yml && conda activate cuddly-waddle`
- **Run Backend**: `cd backend/app && uvicorn main:app --reload`

## Lint Commands
- **Frontend**: `npm run lint`

## Test Commands
- No explicit test commands found. Check with developer if needed.

## Code Style Guidelines
- **Frontend**: 
  - 2-space indentation
  - Semicolons required
  - PascalCase for components, camelCase for variables/functions
  - Functional React components with hooks
  - Chakra UI component library with destructured imports
  - JSX attributes on new lines when numerous

- **Backend**:
  - 4-space indentation
  - Snake_case for functions/variables, PascalCase for classes
  - Type hints required on function parameters and returns
  - Organized imports: stdlib → third-party → local
  - Pydantic models for data validation
  - Docstrings for modules, classes, and functions