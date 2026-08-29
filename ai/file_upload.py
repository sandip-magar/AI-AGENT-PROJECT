import os 
from dotenv import load_dotenv
from db.models import PDFDocument, User
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
import asyncio, tempfile 
from ai.brain import vectorstore, retriever
from routers.auth import get_current_user
from sqlalchemy.sql import func
from langchain_google_genai import GoogleGenerativeAIEmbeddings

router = APIRouter()
MAX_FILE_SIZE = 10 * (1024*1024)

load_dotenv()
embedding = GoogleGenerativeAIEmbeddings(model=os.getenv("EMBEDDING_MODEL_NAME"))

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a PDF.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"File size is too large maximum size: {MAX_FILE_SIZE // (1024*1024)} MB.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    with tempfile.NamedTemporaryFile(delete=False, prefix=".pdf") as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(content)

    try: 
        loader = await asyncio.to_thread(PyPDFLoader, temp_file_path)
        doc = loader.load()

        #split the doc into chunks 
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        chunks = await asyncio.to_thread(splitter.split_documents, doc)

        for doc in chunks:
            doc.metadata['source'] = file.filename
            doc.metadata['category'] = "my_pdf_docs"
            doc.metadata['user_id'] = current_user.id

        full_text = " ".join(doc.page_content for doc in chunks)

        new_document = PDFDocument(
            user_id = current_user.id,
            filename = file.filename,
            temp_file = temp_file_path,
            content = full_text,
            uploaded_at = func.now()
        )

        db.add(new_document)
        db.commit()

        print(f" PDF saved to the DB as ID: '{new_document.id}")

        await asyncio.to_thread(vectorstore.add_documents, chunks)

        return{
            "message": f" PDF File '{file.filename}' processed successfullly !",
            "chunk_processed": len(chunks)
        }

    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error:{str(e)}"
        )

@router.delete("/delete-pdf")
async def delete_pdf(
    filename:str,
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #delete from the database 
    vectorstore.delete(filter={"source":filename})
    document = db.query(PDFDocument).filter(PDFDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    db.delete(document)
    db.commit()

    return {"message": "PDF File Deleted Successfully!"}