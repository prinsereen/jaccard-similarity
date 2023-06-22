import os
import PyPDF2
from nltk.tokenize import word_tokenize
import nltk
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import JSONResponse
import threading
import uvicorn

# Download the "punkt" resource
nltk.download('punkt')

# Create the FastAPI app
app = FastAPI()

def calculate_jaccard_similarity(file1, file2):
    # Extract text from PDF files
    text1 = file1
    text2 = file2

    # Tokenize the text
    tokens1 = set(word_tokenize(text1.lower()))
    tokens2 = set(word_tokenize(text2.lower()))

    # Calculate Jaccard similarity
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    similarity = intersection / union

    return similarity


@app.post('/jaccard-similarity')
async def jaccard_similarity(request: Request):
    try:
        # Retrieve the JSON data from the request
        data = await request.json()
        file1 = data['file1']
        file2 = data['file2']

        # Calculate Jaccard similarity
        similarity = calculate_jaccard_similarity(file1, file2)

        # Return the response as JSON with content type application/json
        return JSONResponse(content={'jaccard_similarity': similarity}, media_type='application/json')

    except Exception as e:
        # Return an error message as JSON with content type application/json
        return JSONResponse(content={'error': str(e)}, media_type='application/json')
