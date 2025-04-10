from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print("📧 EMAIL_USER:", EMAIL_USER)
print("🔐 EMAIL_PASS:", "已讀取" if EMAIL_PASS else "❌ 缺失")

app = FastAPI()

class MailRequest(BaseModel):
    to: str
    subject: str
    content: str = ""
    is_html: bool = False
    template: bool = False
    variables: dict = None

@app.post("/send-mail")
def send_mail(req: MailRequest):
    try:
        print("📨 收到寄信請求:", req.dict())

        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = req.to
        msg["Subject"] = req.subject

        if req.template:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("template.html", "r", encoding="utf-8") as f:
                html = f.read()
            html = html.replace("{{current_time}}", now)

            if req.variables:
                for key, value in req.variables.items():
                    html = html.replace(f"{{{{{key}}}}}", str(value))

            msg.add_alternative(html, subtype='html')
        elif req.is_html:
            msg.add_alternative(req.content, subtype='html')
        else:
            msg.set_content(req.content)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        print("✅ 郵件已成功發送")
        return {"message": "Gmail mail sent successfully!"}
    except Exception as e:
        print("❌ 發信失敗:", str(e))
        raise HTTPException(status_code=500, detail=f"寄信失敗：{str(e)}")