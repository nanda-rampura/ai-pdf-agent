from fastapi import FastAPI, UploadFile, File
import PyPDF2
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI PDF Agent is running 🚀"}

@app.get("/ask-pdf/")
def ask_pdf(question: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer questions based on the provided PDF"},
            {"role": "user", "content": f"PDF Content:\n{pdf_text}\n\nQuestion: {question}"}
        ]
    )

    return {"answer": response.choices[0].message.content}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text

    content = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(content)

    reader = PyPDF2.PdfReader("temp.pdf")
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    pdf_text = text

    return {
        "filename": file.filename,
        "preview": text[:500]
    }