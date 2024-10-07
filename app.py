from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from gradio_client import Client, handle_file
import logging
import uvicorn

# Initialize FastAPI app and enable CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files like index.html, style.css, and script.js
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a client instance for the Hugging Face Space API
client = Client("AIDC-AI/Ovis1.6-Gemma2-9B")

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as f:
        return f.read()

@app.post("/submit_chat")
async def submit_chat(text_input: str = Form(...)):
    logging.info(f"Received text input: {text_input}")
    try:
        # Make the API call
        response = client.predict(
            chatbot=[],
            text_input=text_input,
            api_name="/submit_chat"
        )
        logging.info(f"Full API response: {response}")
        return {"response": response[0][1]}  # Returning the chatbot response text
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return {"response": f"Sorry, I couldn't process your request. Error: {str(e)}"}

@app.post("/process_image")
async def process_image(file: UploadFile):
    file_location = f"/mnt/data/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    logging.info(f"Processing image: {file_location}")
    try:
        # Make the API call with the image
        response = client.predict(
            chatbot=[],
            image_input=handle_file(file_location),
            api_name="/ovis_chat"
        )
        logging.info(f"Full image response from API: {response}")
        return {"response": response[0][1]}  # Extracting and returning the response text
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return {"response": f"Sorry, I couldn't process the image. Error: {str(e)}"}

@app.post("/clear_chat")
async def clear_chat():
    try:
        # Make the API call to clear chat
        response = client.predict(api_name="/clear_chat")
        logging.info(f"Clear chat response: {response}")
        return {"response": "Chat has been cleared."}
    except Exception as e:
        logging.error(f"Error clearing chat: {e}")
        return {"response": f"Sorry, I couldn't clear the chat. Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
