def invoice_analysis_prompt(policy_text: str, invoice_text: str) -> str:
    return f"""
You are an expert HR auditor. Given the HR reimbursement policy and an invoice, analyze the invoice and determine:
1. Reimbursement Status: Fully Reimbursed / Partially Reimbursed / Declined
2. Reason: Justify the status clearly based on the policy.


HR POLICY:
{policy_text}

INVOICE:
{invoice_text}

Give a short summary with Reimbursement Status and Reason.
"""

def chatbot_system_prompt(user_query: str, context_docs: str) -> str:
    return f"""
You are a helpful assistant. Use the following invoice analysis documents to answer the user's query:

Documents:
{context_docs}

Query:
{user_query}

"""
# The above prompt is designed to provide the LLM with the necessary context and user query to generate a relevant response.