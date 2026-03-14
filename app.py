from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import re

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage

from database import init_db, save_chat

load_dotenv()

app = Flask(__name__)

init_db()

api_key = os.getenv("MISTRAL_API_KEY")

model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.7,
    mistral_api_key=api_key
)

messages = []


def detect_privacy_risk(message):

    risks = []

    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b\d{10}\b'
    password_pattern = r'password\s*[:=]\s*\S+'

    if re.search(email_pattern, message):
        risks.append("Email detected")

    if re.search(phone_pattern, message):
        risks.append("Phone number detected")

    if re.search(password_pattern, message.lower()):
        risks.append("Password detected")

    return risks


@app.route("/", methods=["GET", "POST"])
def index():

    warning = ""

    if request.method == "POST":

        user_message = request.form["message"]

        risks = detect_privacy_risk(user_message)

        if risks:
            warning = "Privacy Risk: " + ", ".join(risks)

        try:

            messages.append(HumanMessage(content=user_message))

            response = model.invoke(messages)

            messages.append(AIMessage(content=response.content))

        except Exception as e:

            print("AI Error:", e)

            messages.append(AIMessage(content="AI service unavailable."))

        save_chat(user_message, messages[-1].content, warning)

    # convert messages for HTML
    chat_history = []

    for m in messages:
        if isinstance(m, HumanMessage):
            chat_history.append({"role": "user", "content": m.content})
        elif isinstance(m, AIMessage):
            chat_history.append({"role": "bot", "content": m.content})

    return render_template(
        "index.html",
        chat_history=chat_history,
        warning=warning
    )


if __name__ == "__main__":
    app.run(debug=True)