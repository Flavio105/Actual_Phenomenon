import gradio as gr
import requests

API_URL = "https://llm-invoice-api.onrender.com"


def analyze_invoice(policy_file_path, invoice_zip_path, employee_name):
    try:
        with open(policy_file_path, 'rb') as pf, open(invoice_zip_path, 'rb') as zipf:
            files = {
                'policy_file': ("policy.pdf", pf, 'application/pdf'),
                'invoice_zip': ("invoices.zip", zipf, 'application/zip'),
            }
            data = {'employee_name': employee_name}
            
            response = requests.post(f"{API_URL}/analyze/", files=files, data=data)
            result = response.json()
            
            if "message" in result:
                return result["message"]
            else:
                return f" Error: {result.get('error', 'Unknown error occurred.')}"
    except Exception as e:
        return f"Exception: {str(e)}"


def chat_with_bot(query):
    response = requests.post(f"{API_URL}/chat/", data={"query": query})
    result = response.json()
    
    if "error" in result:
        return f"Error: {result['error']}"
    return result.get("response", "Error: No response from LLM.")


def create_gradio_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("## Invoice Reimbursement Analyzer & Chatbot Assistant")

        with gr.Tab(" Invoice Analysis"):
            with gr.Row():
                policy_file = gr.File(label=" Upload HR Policy PDF", type="filepath", file_types=[".pdf"])
                invoice_zip = gr.File(label=" Upload Invoices ZIP", type="filepath", file_types=[".zip"])
            employee_name = gr.Textbox(label="👤 Employee Name", placeholder="Enter employee name")
            analyze_button = gr.Button("🔍 Analyze Invoices")
            analyze_output = gr.Textbox(label=" Analysis Result")

            analyze_button.click(analyze_invoice, inputs=[policy_file, invoice_zip, employee_name], outputs=analyze_output)

        with gr.Tab("Chatbot"):
            query = gr.Textbox(label="💡 Ask about invoices (e.g., 'Invoices for Ramesh with Partially Reimbursed status')")
            chat_button = gr.Button("🤖 Ask Chatbot")
            chatbot_output = gr.Textbox(label="Chatbot Response")

            chat_button.click(chat_with_bot, inputs=[query], outputs=chatbot_output)

    demo.launch()

if __name__ == "__main__":
    create_gradio_interface()
