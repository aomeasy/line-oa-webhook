from fastapi import FastAPI, Request
import requests

app = FastAPI()

LINE_CHANNEL_ACCESS_TOKEN = "iMsTkrXbgOPkks0jJnllv5cSaYB31upP34SvxzIsJ/+2MDlHsI89Rp5BhzKCpWOc9hDoIjDFd5LMN5n4n38e/cI0w32vYNfWRvO4uI2zAJLwNXOdL5fWDY2pTgaql2GFEWLJ5I5K3dOThgYmMzxKAAdB04t89/1O/w1cDnyilFU="
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def line_webhook(req: Request):
    body = await req.json()
    events = body.get("events", [])

    for event in events:
        if event.get("type") == "message":
            reply_token = event["replyToken"]
            user_msg = event["message"].get("text", "")
            reply(user_msg, reply_token)

    return {"status": "processed"}

def reply(text: str, reply_token: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    r = requests.post(LINE_REPLY_URL, headers=headers, json=data)
    return r.json()
