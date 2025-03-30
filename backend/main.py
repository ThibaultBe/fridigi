import io
import pytesseract
from fastapi import FastAPI, UploadFile
from PIL import Image
from dotenv import load_dotenv, dotenv_values
from langchain_mistralai import ChatMistralAI

# Load environment variables from .env file
load_dotenv()

# Initialize model
model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    max_retries=2,
    api_key=dotenv_values().get("MISTRAL_API_KEY"),
)

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """Upload a file and perform OCR on it."""
    
    # Read image data and convert to PIL Image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    # Perform OCR
    text = pytesseract.image_to_string(image)

    # Prepare messages for the model
    messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    (
        "human",
        "I love programming."
    ),
    ]

    text = model.invoke(messages)
    
    return {"filename": file.filename, "text": text}