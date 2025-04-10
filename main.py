from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

# 載入 .env 檔案中的環境變數
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = FastAPI()

# 請求格式：只包含 to, subject, content
class MailRequest(BaseModel):
    to: str
    subject: str
    content: str

@app.post("/send-mail")
def send_mail(req: MailRequest):
    try:
        # 建立 EmailMessage 物件
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = req.to
        msg["Subject"] = req.subject
        msg["content"](req.content)  # 純文字內容

        # 發送郵件（Outlook）
        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return {"message": "Outlook mail sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
