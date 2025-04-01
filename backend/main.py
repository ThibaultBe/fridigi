from fastapi import FastAPI, UploadFile
from PIL import Image
import time
import io

# Agent assistant
from langchain_core.messages import AnyMessage, SystemMessage
from langchain.schema import HumanMessage, AIMessage
# Models
from langchain_mistralai import ChatMistralAI
import pytesseract
# Graphing imports
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
# Custom imports for the assistant
from typing import TypedDict, List, Dict, Any, Optional

# Load environment variables from .env file
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM.
model=ChatMistralAI(model="mistral-small-latest", temperature=0, max_retries=2, api_key=dotenv_values().get("MISTRAL_API_KEY"))

# Initialize the FastAPI app
app = FastAPI()

# Define the state
class ReceiptState(TypedDict):
    extracted_text: str
    is_grocery: Optional[bool]      
    draft_response: Optional[str]
    messages: List[Dict[str, Any]]

# -- Define our nodes -- #
def read_receipt(state: ReceiptState):
    extracted_text = state["extracted_text"]
    # We don't alter the state, so we return it unchanged
    return {}

def classify_receipt(state: ReceiptState):
    """
    Classify the receipt as spam or not.
    """
    # Dummy classification logic
    extracted_text = state["extracted_text"]
    prompt = f"""
    As assistant, analyze the receipt text and determine if it is a grocery list or not.

    The receipt text is: {extracted_text}

    Answer with NOT_GROCERY or GROCERY if it's a grocery list. Only return the answer.
    Answer : 
    """
    
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    response_text = response.content.lower()
    print(response_text)
    is_grocery = "grocery" in response_text and "not_grocery" not in response_text

    if not is_grocery:
        new_messages = state.get("messages", []) + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response.content},
        ]
    else:
        new_messages = state.get("messages", [])

    return {
        "is_grocery": is_grocery,
        "messages": new_messages,
    }

def handle_non_grocery(state: ReceiptState):
    print(f"Assistant has marked the receipt as non-grocery.")
    print("The assistant will not process the receipt further.")
    return {}

def drafting_response(state: ReceiptState):
    time.sleep(2)
    extract_text = state["extracted_text"]

    prompt = f"""
    As assistant, draft a list of ingredients from the receipt text and their quantity

    The receipt text is: {extract_text}

    Draft a list of ingredients and their quantity.
    """

    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content},
    ]

    return {
        "draft_response": response.content,
        "messages": new_messages,
    }

def notify_user(state: ReceiptState):
    print("\n" + "="*50)
    print("Sir, you've received a receipt ticket from.")
    print("-"*50)
    print(state["draft_response"])
    print("\n" + "="*50)
    
    return {}

# Routing logic
def route_receipt(state: ReceiptState) -> str:
    """
    Route the receipt based on classification.
    """
    if state["is_grocery"]:
        return "grocery"
    else:
        return "not_grocery"

# Create the graph
receipt_graph = StateGraph(ReceiptState)

# Add nodes
receipt_graph.add_node("read_receipt", read_receipt) # these nodes will execute their specific functions
receipt_graph.add_node("classify_receipt", classify_receipt)
receipt_graph.add_node("handle_non_grocery", handle_non_grocery)
receipt_graph.add_node("drafting_response", drafting_response)
receipt_graph.add_node("notify_user", notify_user)

# Define routing edges
receipt_graph.add_edge(START, "read_receipt") # After the start, we read the receipt
receipt_graph.add_edge("read_receipt", "classify_receipt") # After reading, we classify the receipt
receipt_graph.add_conditional_edges(
    "classify_receipt", # After classify, we run the "route_receipt" function
    route_receipt, 
    {
        "not_grocery": "handle_non_grocery",
        "grocery": "drafting_response",
    }
)

# Add the final edges
receipt_graph.add_edge("handle_non_grocery", END) # After handling non-grocery, we end
receipt_graph.add_edge("drafting_response", "notify_user") # After drafting a list response, we notify the user
receipt_graph.add_edge("notify_user", END) # After notifying the user, we end

compiled_graph = receipt_graph.compile()


image = Image.open("walmart.png")
# Perform OCR using pytesseract
text = pytesseract.image_to_string(image)
print("This is the retrieved OCR: ", text)
retrieved_text = compiled_graph.invoke(
    {
        "extracted_text": text,
        "is_grocery": None,
        "spam_reason": None,
        "messages": [],
    }
)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """
    Receive an image file, perform OCR to extract text, and return the text.
    
    Args:
        file (UploadFile): The uploaded image file.
    Returns:
        dict: A dictionary containing the filename and extracted text.
    """
    # Read image data and convert to PIL Image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)
    
    
    retrieved_text = compiled_graph.invoke(
        {
            "extracted_text": text,
            "is_grocery": None,
            "spam_reason": None,
            "messages": [],
        }
    )
    
    return {"filename": file.filename, "text": retrieved_text}