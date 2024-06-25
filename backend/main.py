from fastapi import FastAPI, File, UploadFile
from opensearchpy import OpenSearch
from pypdf import PdfReader
from datetime import datetime
import os 
import shutil
import uuid

app = FastAPI()


def extract_and_index_pdf(pdf_path: str, opensearch_client: OpenSearch, index_name):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        document_id = uuid.uuid4()
        for i, page in enumerate(reader.pages):
            page_num = i + 1
            text_in_page = page.extract_text() if page.extract_text() else ""
            document = {
                "document_id": document_id,
                "page_number": page_num,
                "title": os.path.splitext(os.path.basename(pdf_path)),
                "registration_date": datetime.now().isoformat(),
                "content": text_in_page
            }
            opensearch_client.index(index=index_name, body=document)

@app.post("/upload/")
async def register_pdf_as_document(file: UploadFile = File(...)):
    tmp_path = f"backend/temp/{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
        verify_certs=False
    )

    extract_and_index_pdf(pdf_path=tmp_path, opensearch_client=client, index_name="upload_test_index")
    os.remove(tmp_path)
    return {"filename": file.filename}