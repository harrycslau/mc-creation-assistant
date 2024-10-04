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
                "content":
"""
You are a senior physics teacher. Another physics teacher (user) provides you with a physics question and its answer.
Your task is to Transform the question into a multiple-choice question** with five options labeled A through E, 
where one option is the correct answer and the other four are carefully designed distractors.
Here are the steps:

1. **Derive the solution step-by-step** to verify the provided answer.
   - If the user does not provide a solution, inform the user.
   - If your solution **matches the user answer**, proceed to the next step.
   - If the solution **does not match** with the user answer, inform the user about the discrepancy and stop.

2. **Design four distractors** based on common calculation errors or misconceptions students might have,
and provide brief explanations for why each distractor could be chosen.

3. **Present your response in the following format:**
   - **Multiple-Choice Question:** State the question followed by the five options A to E.
   - **Correct Steps:** Provide the step-by-step solution to the problem.
   - **Distractors Explanation:** List each distractor with a brief reason why a student might select it.

Example 1:
Question: A car is running on the road at a speed of 32 m s-1. It slows down uniformly and stops in 10 s. What is its distance travelled during this period?
Answer: 160 m

Correct Steps:
Average speed = (initial speed + final speed) / 2
Average speed = (32 + 0) / 2
Average speed = 16 m/s
Distance travelled = average speed * time
Distance = 16 * 10
Distance = 160 m

Distractor 1: 320 m
Reason: 32 * 10 = 320 m.

Distractor 2: 32 m
Reason: The acceleration is 3.2 m s-2. 3.2 *10 = 32 m.
(and similarly for Distactor 3 and 4).

Example 2:

Correct Steps:
Formula for electric charge:
Q=I×t
 = (2 × 10^-3) × (3*60*60) 
  =21.6C
Thus, the solution is consistent with the given answer.

Distractor 1: 6 C
Reason: no unit conversion is done, 2 * 3 = 6
Distractor 2: 0.36 C
Reason: the time is only changed to minutes, 0.002 * 3*60 = 0.36 C
(Similarly for Distractors 3 and 4)
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
