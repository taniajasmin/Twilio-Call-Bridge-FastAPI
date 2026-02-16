from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, Response, JSONResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os
from fastapi import Request

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

call_state = {
    "status": "idle"
}

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
    call_state["status"] = "calling_a"

    # call = client.calls.create(
    #     to=person_a,
    #     from_=TWILIO_NUMBER,
    #     url=f"{BASE_URL}/twilio-webhook"
    # )

    # return JSONResponse({
    #     "success": True,
    #     "call_sid": call.sid
    # })

    call = client.calls.create(
        to=person_a,
        from_=TWILIO_NUMBER,
        url=f"{BASE_URL}/twilio-webhook",
        status_callback=f"{BASE_URL}/status-callback",
        status_callback_event=["initiated", "ringing", "answered", "completed"],
        status_callback_method="POST"
    )

    return {"success": True}


# @app.api_route("/twilio-webhook", methods=["GET", "POST"])
# def twilio_webhook():

#     response = VoiceResponse()

#     # Connect second person
#     response.dial(
#         call_data["person_b"],
#         callerId=TWILIO_NUMBER
#     )

#     return Response(
#         content=str(response),
#         media_type="application/xml"
#     )

@app.api_route("/twilio-webhook", methods=["GET", "POST"])
def twilio_webhook():

    call_state["status"] = "calling_b"

    response = VoiceResponse()

    response.dial(
        call_data["person_b"],
        callerId=TWILIO_NUMBER
    )

    return Response(str(response), media_type="application/xml")


@app.post("/status-callback")
async def status_callback(request: Request):
    form = await request.form()
    call_status = form.get("CallStatus")

    if call_status == "completed":
        call_state["status"] = "completed"

    return {"ok": True}

@app.get("/call-status")
def get_status():
    return call_state