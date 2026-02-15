from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, Response, JSONResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Twilio Human Call Bridge")

# ENV VARIABLES
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
BASE_URL = os.getenv("BASE_URL")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# temporary storage
call_data = {}


@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/make-call")
async def make_call(
    person_a: str = Form(...),
    person_b: str = Form(...)
):
    """
    Twilio calls Person A first,
    then connects Person B.
    """

    call_data["person_b"] = person_b

    call = client.calls.create(
        to=person_a,
        from_=TWILIO_NUMBER,
        url=f"{BASE_URL}/twilio-webhook"
    )

    return JSONResponse({
        "success": True,
        "call_sid": call.sid
    })


@app.api_route("/twilio-webhook", methods=["GET", "POST"])
def twilio_webhook():

    response = VoiceResponse()

    # Connect second person
    response.dial(
        call_data["person_b"],
        callerId=TWILIO_NUMBER
    )

    return Response(
        content=str(response),
        media_type="application/xml"
    )
