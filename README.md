# Twilio Human Call Bridge (FastAPI)

## Overview

This project is a simple FastAPI application that uses Twilio to connect two people through a phone call.

The system acts as a bridge:

1. Twilio calls **Person A**
2. After Person A answers, Twilio calls **Person B**
3. Both people are connected and can talk normally

There are no AI agents or automated voice systems. Twilio only connects two humans.

---

## Call Flow
```txt
User clicks "Start Call"
↓
Twilio calls Person A
↓
Person A answers
↓
Twilio calls Person B
↓
Both parties are connected
```

Twilio remains in the middle and manages the connection.

---

## Project Structure
```txt
project/
│
├── main.py # FastAPI backend
├── index.html # Simple frontend form
├── .env # Environment variables
└── requirements.txt
```

---

## Requirements

- Python 3.10+
- Twilio Account
- Twilio Phone Number
- ngrok (for public webhook access)

---

## Installation

### 1. Clone the repository
```json
git clone https://github.com/taniajasmin/Twilio-Call-Bridge-FastAPI-.git
cd <repo folder>
```

### 2. Install dependencies
```json
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.
```txt
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
BASE_URL=http://productionurl
```

### Notes

- `TWILIO_PHONE_NUMBER` is the number purchased from Twilio.
- `BASE_URL` must be publicly accessible.
- Do not use localhost for webhooks.

---

## Running the Application

### Start FastAPI
```txt
uvicorn main:app --reload
```

### Server runs at:
```txt
http://localhost:8000
```

---

### Start ngrok

Expose the local server:
```txt
ngrok http 8000
```

Copy the HTTPS URL and update `BASE_URL` inside `.env`.

Restart FastAPI after updating `.env`.

---

## Using the Application

1. Open the browser:
```txt
http://localhost:8000
```

2. Enter phone numbers:

- **Person A** – called first
- **Person B** – connected second

3. Click **Start Call**

Twilio will:
- Call Person A
- After answer, call Person B
- Connect both calls together

---

## Important Notes

- Person A and Person B must be different phone numbers.
- Testing with the same phone number will result in a busy signal.
- Twilio must be able to reach your webhook through a public URL.

---

## Dependencies

fastapi
uvicorn
twilio
python-dotenv
python-multipart


---

## Limitations (Demo Version)

This project stores call data temporarily in memory.  
It is intended for testing and learning purposes only. 

For production usage, consider:
- Database storage
- Call SID mapping
- Authentication
- Error handling and logging

---

## License

This project is provided for educational and testing purposes. Because my company is too posh to recharge local SIMs for testing.
