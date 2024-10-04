# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
app = FastAPI()

# Allow CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://groq.helicone.ai/",
    default_headers={
        "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}",
    }
)

@app.get("/api/hello")
async def say_hello():
    return {"message": "hello world"}


@app.post("/api/phymc-generate")
async def generate(data: dict):
    user_content = data.get("question") + " Answer: " + data.get("answer")
    chat_completion = client.chat.completions.create(
        model="llama-3.2-11b-text-preview",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": """
                You are a senior physics teacher. Comment on whether the user's question difficulty is suitable for which grade.
                """
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.6,
    )

    result = chat_completion.choices[0].message.content
    return {"response": result}
