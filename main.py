from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print("📧 EMAIL_USER:", EMAIL_USER)
print("🔐 EMAIL_PASS:", "已讀取" if EMAIL_PASS else "❌ 缺失")

app = FastAPI()

class MailRequest(BaseModel):
    to: str
    subject: str
    content: str

@app.get("/")
def root():
    return {"message": "SendMail API is up. Try POST /send-mail"}

@app.post("/send-mail")
def send_mail(req: MailRequest):
    try:
        print("📨 收到寄信請求:", req.dict())
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = req.to
        msg["Subject"] = req.subject
        msg.set_content(req.content)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        print("✅ 郵件已成功發送")
        return {"message": "Outlook mail sent successfully!"}
    except Exception as e:
        print("❌ 發信失敗:", str(e))
        raise HTTPException(status_code=500, detail=f"寄信失敗：{str(e)}")
