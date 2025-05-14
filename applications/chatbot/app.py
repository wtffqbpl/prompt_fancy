#! coding: utf-8

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from applications.chatbot.dialog_manager import determine_state, build_prompt
from applications.chatbot.memory import save_chat_history
from utils.tools import get_completion


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get('user_id', 'default_user')
    user_input = data.get('message', '')

    state = determine_state(user_input)
    prompt = build_prompt(user_id, user_input, state)
    # FIXME: Specify the model name
    response, _ = get_completion(prompt)

    # Save chat history and user memory
    save_chat_history(user_id, "user", user_input)
    save_chat_history(user_id, "assistant", response)

    return {"response": response}


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
