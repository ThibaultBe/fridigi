import io
import pytesseract
from fastapi import FastAPI, UploadFile
from PIL import Image

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """Upload a file and perform OCR on it."""
    # Read image data and convert to PIL Image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    # Perform OCR
    text = pytesseract.image_to_string(image)
    
    return {"filename": file.filename, "text": text}