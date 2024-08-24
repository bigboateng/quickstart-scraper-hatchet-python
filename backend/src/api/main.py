from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
from dotenv import load_dotenv

# Import the Hatchet SDK
from hatchet_sdk import Hatchet

# Load environment variables from a .env file
load_dotenv()

# Initialize Hatchet with the API key from environment variables
hatchet = Hatchet()

app = FastAPI()

# Define the allowed origins for CORS (in this case, allowing localhost from frontend)
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# Apply CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Basic route to confirm the API is working
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hatchet Scraper API!"}

# Endpoint to initiate a scraping workflow
@app.post("/scrape")
async def scrape():
    # Trigger the Hatchet workflow named "ScraperWorkflow"
    workflowRun = await hatchet.client.admin.aio.run_workflow("ScraperWorkflow", {})
    
    # Return the unique ID of the workflow run to track its progress
    return {
        "messageId": workflowRun.workflow_run_id,
    }

# Generator function to stream events from a Hatchet workflow
async def event_stream_generator(workflowRunId):
    # Retrieve the workflow run using its ID
    workflowRun = hatchet.client.admin.get_workflow_run(workflowRunId)

    # Stream each event emitted by the workflow in real-time
    async for event in workflowRun.stream():
        # Format the event data to be sent to the client
        data = json.dumps({
            "type": event.type,
            "payload": event.payload,
            "messageId": workflowRunId
        })
        yield "data: " + data + "\n\n"

    # Once the workflow completes, get the final result
    result = await workflowRun.result()

    # Send the final result to the client
    data = json.dumps({
        "type": "result",
        "payload": result,
        "messageId": workflowRunId
    })

    yield "data: " + data + "\n\n"

# Endpoint to stream workflow events based on the message ID
@app.get("/message/{messageId}")
async def stream(messageId: str):
    # In this case, the message ID is used directly as the workflow run ID
    workflowRunId = messageId
    return StreamingResponse(event_stream_generator(workflowRunId), media_type='text/event-stream')

# Function to start the FastAPI application with uvicorn
def start():
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
