# Hatchet Scraper Example

This project demonstrates a web scraping application using FastAPI for the backend API, Next.js for the frontend, and Hatchet for task management and workflow orchestration. It showcases the power and flexibility of Hatchet in managing complex workflows for web scraping tasks.

## Key Features

- Multiple workflows: Separate workflows for scraping Google News and TechCrunch
- Child workflows: Main workflow spawns child workflows for each scraping task
- Real-time updates: Utilizes streaming to get live workflow data
- Web scraping: Demonstrates scraping techniques using Beautiful Soup

## Quick Start

To get the project running quickly:

1. Clone the repository
2. Copy the pre-filled environment file:
   ```bash
   cp backend/.env.template backend/.env
   ```
3. Set up your Hatchet API Key in the `.env` file (see Environment Setup section)
4. Run the start-all script:
   ```bash
   ./start-all.sh
   ```

This will start the FastAPI server, Hatchet worker, and Next.js frontend.

## Manual Setup

If you prefer to start services individually:

1. Install dependencies (if not already installed):
   ```bash
   cd backend
   poetry install  # Run this only if you haven't installed dependencies yet
   ```

2. Start the FastAPI server:
   ```bash
   cd backend
   poetry run start-api
   ```

3. Start the Hatchet worker:
   ```bash
   cd backend
   poetry run start-worker
   ```

4. Start the Next.js frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## Usage

Once the services are running, open your browser and navigate to `http://localhost:3000`. You can initiate scraping tasks and view the results in real-time.

## Project Structure

- `backend/`: FastAPI server and Hatchet workflows
- `frontend/`: Next.js frontend application


## Environment Setup

Before running the project, you need to configure your environment variables. We've provided a `.env.template` file to guide you through the process.

### Steps to Set Up the Environment

1. **Copy the `.env.template` file to create a `.env` file**:

   ```bash
   cp backend/.env.template backend/.env
   ```

2. **Get your Hatchet API Key**:
   - Navigate to your settings tab in the Hatchet dashboard.
   - Look for the section called "API Keys".
   - Click "Create API Key" and input a name for the key.
   - Copy the generated API key.

3. **Fill in the values for the environment variables**:

   `HATCHET_CLIENT_TOKEN`: Paste your Hatchet API key here.

4. Save the `.env` file. Ensure that it remains in the backend directory, as this is where the application expects it.

### Important Notes

Do not commit your `.env` file to version control. The `.env` file contains sensitive information like tokens and passwords. We've already included `.env` in the `.gitignore` file to prevent it from being accidentally committed.