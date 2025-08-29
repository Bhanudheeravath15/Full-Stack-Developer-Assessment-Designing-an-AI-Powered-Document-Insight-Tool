from fastapi import FastAPI, UploadFile, File
import uvicorn
import fitz  # PyMuPDF for PDF text extraction

app = FastAPI()

# extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    text = extract_text_from_pdf(file.file)

    # Fallback "summary" = top 5 words
    words = text.split()
    summary = " ".join(words[:50])  # just first 50 words for now

    return {
        "filename": file.filename,
        "summary": summary,
        "total_words": len(words)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
