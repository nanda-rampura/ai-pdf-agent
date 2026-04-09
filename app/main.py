from fastapi import FastAPI, UploadFile, File
import PyPDF2

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI PDF Agent is running 🚀"}


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(content)

    reader = PyPDF2.PdfReader("temp.pdf")
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return {
        "filename": file.filename,
        "preview": text[:500]
    }