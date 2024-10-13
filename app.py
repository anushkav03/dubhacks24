from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List, Dict
from llm import chatbot_with_memory  # Assuming this function sends requests to LLM (e.g., GPT)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

class PromptInput(BaseModel):
    prompt: str

class ThemeInput(BaseModel):
    theme: str

@app.post("/generatePrompts")
async def generate_prompts(theme_input: ThemeInput):
    theme = theme_input.theme.lower()

    try:
        # Construct a clear and specific prompt to generate engaging prompts for the theme
        prompt_request = (
            f"Generate two distinct and engaging speaking prompts based on the theme '{theme}'. "
            "Ensure that each prompt is clear, concise, and easy to understand. "
            "Return the two prompts separated by a newline character."
        )

        # Assuming `chatbot_with_memory` sends this request to the LLM (e.g., GPT)
        conversation_history = []  # Empty history for fresh prompt generation
        response = chatbot_with_memory(conversation_history, prompt_request)

        # Split the LLM response by newline to separate the two prompts
        prompts = response[0].split("\n")

        # Clean the prompts to ensure they are not empty and properly formatted
        prompts = [prompt.strip() for prompt in prompts if prompt.strip()]

        # Return only the first two prompts in the response
        return {"prompts": prompts[:2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate prompts from LLM")


@app.post("/postToClaude")
async def send_to_claude(request: MessageRequest):
    user_input = request.message
    try:
        # Send user input to Claude via Bedrock (replace this with actual logic)
        conversation_history = []
        response = chatbot_with_memory(conversation_history, user_input)[0]
        return {"reply": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to connect to Claude API")

@app.post("/generateParagraph")
async def generate_paragraph(request: PromptInput):
    prompt = request.prompt

    try:
        # Send the selected prompt to the LLM to generate a paragraph
        paragraph_request = f"Write a detailed paragraph based on the following prompt: {prompt}."
        conversation_history = []
        response = chatbot_with_memory(conversation_history, paragraph_request)

        # Return the generated paragraph (assuming it's in the first part of the response)
        return {"paragraph": response[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate paragraph from LLM")



# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
