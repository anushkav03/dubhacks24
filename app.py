from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Dict
from llm import chatbot_with_memory  # Assuming this function sends requests to LLM (e.g., GPT)
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import os
import uuid

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
        prompt_request = (
            f"Generate two distinct and engaging speaking prompts based on the theme '{theme}'. "
            "Ensure that each prompt is clear, concise, and easy to understand. "
            "Return the two prompts separated by a newline character."
        )
        conversation_history = []  # Empty history for fresh prompt generation
        response = chatbot_with_memory(conversation_history, prompt_request)
        prompts = response[0].split("\n")
        prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
        return {"prompts": prompts[:2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate prompts from LLM")

@app.post("/postToClaude")
async def send_to_claude(request: MessageRequest):
    user_input = request.message
    try:
        conversation_history = []
        response = chatbot_with_memory(conversation_history, user_input)[0]
        return {"reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to connect to Claude API")

@app.post("/generateParagraph")
async def generate_paragraph(request: PromptInput):
    prompt = request.prompt

    try:
        paragraph_request = f"Write a detailed paragraph based on the following prompt: {prompt}. Ensure your generated prompt is 50 words MAX."
        conversation_history = []
        response = chatbot_with_memory(conversation_history, paragraph_request)
        generated_paragraph = response[0]

        # Now call the text-to-speech conversion using the generated paragraph
        tts = gTTS(text=generated_paragraph, lang="en")
        
        # Save the generated speech to a file
        file_name = f"speech_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join("/tmp", file_name)  # Use a temp directory

        tts.save(file_path)
        print("I saved")

        # Return the generated paragraph along with the audio file
        return {"paragraph": response[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate paragraph or convert to speech")

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)