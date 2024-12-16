import assemblyai as aai
from fastapi import FastAPI, HTTPException
from model import TranscriptionRequest
from lib import generate_config_from_request, generate_response, generate_response_download
from starlette.staticfiles import StaticFiles
from clean_file import start_cleaning_thread
import pymongo
from pymongo import MongoClient
from mongo_utils import process_transcription_data
import os

URL_TEMP = "./temp"
time_interval = 3600  # in seconds

# Initialize FastAPI app
app = FastAPI()
aai.settings.api_key = "edd915cdc8014f9db7190b8a38c0ff28"
headers = {"authorization": "edd915cdc8014f9db7190b8a38c0ff28"}
app.mount("/temp", StaticFiles(directory="temp"), name="static")

# MongoDB connection setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client.transcriptions_db  # Use a database named 'transcriptions_db'
collection = db.transcriptions  # Use a collection named 'transcriptions'

def save_to_mongo(response, audio_url):
    processed_data = process_transcription_data(response, audio_url)
    collection.insert_one(processed_data)
    print("Data saved to MongoDB successfully!")

@app.post("/parse")
async def parse(request: TranscriptionRequest):
    transcriber = aai.Transcriber()

    # Prevent both summarization and auto chapters from being active at the same time
    if request.summarization:
        request.auto_chapters = False
    elif request.auto_chapters:
        request.summarization = False

    # Generate the transcription configuration based on the request
    config = generate_config_from_request(request)

    try:
        # Transcribe the audio using the provided configuration
        transcript = transcriber.transcribe(request.audio_url, config)
        
        # Generate the response based on the transcript and request
        response = generate_response(transcript, request)

        # Save the transcription data into MongoDB
        save_to_mongo(response, request.audio_url)

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/download")
async def download(request: TranscriptionRequest):
    transcriber = aai.Transcriber()
    try:
        # Transcribe the audio using the provided configuration
        transcript = transcriber.transcribe(request.audio_url)

        response = generate_response_download(transcript)

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Start the cleaning thread
cleaning_thread = start_cleaning_thread(URL_TEMP, time_interval)