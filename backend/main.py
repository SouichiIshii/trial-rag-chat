from fastapi import FastAPI, File, UploadFile
from opensearchpy import OpenSearch
from pypdf import PdfReader
from datetime import datetime
import os 
import shutil
import uuid
from opensearch.fetch_all_documents import fetch_all_documents
from opensearch.config import INDEX_NAME

app = FastAPI()


def extract_and_index_pdf(pdf_path: str, opensearch_client: OpenSearch, index_name):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        file_id = uuid.uuid4()
        for i, page in enumerate(reader.pages):
            page_num = i + 1
            text_in_page = page.extract_text() if page.extract_text() else ""
            document = {
                "file_id": file_id,
                "page_number": page_num,
                "title": os.path.basename(pdf_path),
                "registration_date": datetime.now().isoformat(),
                "content": text_in_page
            }
            opensearch_client.index(index=index_name, body=document)

@app.get("/documents/")
def get_unique_documents():
    documents = fetch_all_documents(index_name=INDEX_NAME)

    unique_docs = {}
    for doc in documents:
        source = doc["_source"]
        title = source["title"]
        if title not in unique_docs:
            unique_docs[title] = {
                "title": title,
                "registration_date": source["registration_date"]
            }

    return list(unique_docs.values())

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

    extract_and_index_pdf(pdf_path=tmp_path, opensearch_client=client, index_name=INDEX_NAME)
    os.remove(tmp_path)
    return {"filename": file.filename}