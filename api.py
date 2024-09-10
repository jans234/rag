from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import pak_law_gpt

# Initialize FastAPI app
app = FastAPI()

# Define a Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

# FastAPI endpoint for the chatbot
@app.post("/ask-law")
async def ask_law(question_request: QuestionRequest):
    question = question_request.question

    try:
        # Use the pak_law_gpt function to get the response
        answer = pak_law_gpt(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "PakLaw GPT Chatbot is running!"}
