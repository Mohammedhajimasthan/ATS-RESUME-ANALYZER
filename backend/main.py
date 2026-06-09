from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.ai_engine import analyze_resume
import PyPDF2
import os

app = FastAPI(title="ATSense AI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)

def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    return file.file.read().decode("utf-8")

@app.post("/analyze")
async def analyze(
    resume_file: UploadFile = File(None),
    resume_text: str = Form(""),
    job_description: str = Form("")
):
    text = resume_text
    if resume_file:
        text = extract_text(resume_file)

    result = analyze_resume(text, job_description)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
