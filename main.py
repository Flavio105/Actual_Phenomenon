# I am imorting necessary libraries and modules
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os, zipfile, uuid, datetime
from utils import extract_text_from_pdf, extract_text_from_docx, unzip_and_get_pdfs
from prompts import invoice_analysis_prompt, chatbot_system_prompt
from vector_store import add_to_vector_store, query_vector_store
from groq_llm import call_groq_llm

app = FastAPI()
@app.post("/analyze/") # this is the endpoint of the api call that I did for the invoice analysis
async def analyze(policy_file: UploadFile = File(...), invoice_zip: UploadFile = File(...), employee_name: str = Form(...)):
    try: #if the employee name is provided or not I have written this code to check
        os.makedirs("policy", exist_ok=True)
        policy_path = os.path.join("policy", policy_file.filename)
        with open(policy_path, "wb") as f:
            f.write(await policy_file.read())
        # for extracting the text , policy file (given it in pdf format)
        policy_text = (
            extract_text_from_pdf(policy_path)
            if policy_path.lower().endswith(".pdf")
            else extract_text_from_docx(policy_path)
        )
        print("📃 Policy text:", policy_text[:200])

        invoice_dir = f"invoices/temp_{uuid.uuid4().hex}"
        os.makedirs(invoice_dir, exist_ok=True)
        zip_path = os.path.join(invoice_dir, "invoices.zip")
        with open(zip_path, "wb") as f:
            f.write(await invoice_zip.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(invoice_dir)

        pdf_files = unzip_and_get_pdfs(invoice_dir)
        # checking if the pdf files are present or not

        for pdf in pdf_files:
            invoice_text = extract_text_from_pdf(pdf)
            print(" Invoice text:", invoice_text[:200])

            prompt = invoice_analysis_prompt(policy_text, invoice_text)
            print("Prompt sent to Groq:", prompt[:300])

            llm_response = await call_groq_llm(prompt)
            # print the response from the llm 
            doc_id = uuid.uuid4().hex
            metadata = {
                "employee_name": employee_name,
                "invoice_filename": os.path.basename(pdf),
                "date": str(datetime.date.today())
            }

            full_content = invoice_text + "\n\n" + llm_response
            add_to_vector_store(doc_id, full_content, metadata)

        return JSONResponse(content={"message": "Invoice analysis completed."}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/chat/") # this is the endpoint of the api call that I did for the chatbot
async def chat(query: str = Form(...)):
    try:
        if not query.strip():
            return JSONResponse(content={"error": "Query cannot be empty"}, status_code=400)

        results = query_vector_store(query)
        if not results:
            return JSONResponse(content={"error": "No results found for the query."}, status_code=404)
        # creating a context for the results after joining with the seperator

        context = "\n\n---\n\n".join(results)
        prompt = chatbot_system_prompt(query, context)
        response = await call_groq_llm(prompt)

        return JSONResponse(content={"response": response}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
