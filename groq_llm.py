import httpx # Importing httpx for asynchronous HTTP requests
GROQ_API_KEY = "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"
#placeholder of the api key 
async def call_groq_llm(prompt: str, model: str = "meta-llama/llama-4-scout-17b-16e-instruct", temperature: float = 0.2) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    # Construct the payload for the Groq API request
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 1000
    }
    # Using httpx for asynchronous HTTP requests
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            print("Groq API Error Response:", response.text)
            response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
