# Hatchet Scraper Quickstart

This project is a quick-start example for building a web scraping API using FastAPI (or Flask) and Hatchet for task management. The project is initialized and managed with Poetry, which handles dependencies and environment configuration.

The backend is built in Python and serves as the API that triggers web scraping tasks, utilizing Beautiful Soup for parsing content from Hacker News. Hatchet is integrated to demonstrate workflow features like batch processing and status updates.

This setup aims to provide a straightforward and well-documented starting point for developers looking to build a scraping service with modern Python tools.

## Environment Setup

Before running the project, you need to configure your environment variables. We’ve provided a `.env.template` file to guide you through the process.

## Steps to Set Up the Environment

1. **Copy the `.env.template` file to create a `.env` file**:

   ```bash
   cp backend/.env.template backend/.env

## Fill in the values for the environment variables:

`HATCHET_CLIENT_TOKEN`: Replace "your-hatchet-cloud-token" with your actual Hatchet Cloud token. This token is required to connect to Hatchet Cloud services.
Save the .env file. Ensure that it remains in the backend directory, as this is where the application expects it.

### Important Notes
Do not commit your .env file to version control. The .env file contains sensitive information like tokens and passwords. We've already included .env in the .gitignore file to prevent it from being accidentally committed.
