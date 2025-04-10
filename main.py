from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = FastAPI()

class MailRequest(BaseModel):
    to: str
    subject: str
    content: str

@app.post("/send-mail")
def send_mail(req: MailRequest):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = req.to
        msg["Subject"] = req.subject
        msg.set_content(req.content)

        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return {"message": "Outlook mail sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))