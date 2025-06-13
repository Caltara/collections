import streamlit as st
from twilio.rest import Client  # ✅ Add this line

TWILIO_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = st.secrets["TWILIO_PHONE_NUMBER"]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, name, amount, due_date):
    message = f"Hi {name}, this is a friendly reminder from Caltara. You have an unpaid invoice of ${amount} due on {due_date}. Please reply or call to arrange payment."
    return client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=to
    )

def send_voice(to, name, amount, due_date):
    twiml = f"""
    <Response>
        <Say voice="Joanna" language="en-US">
            Hi {name}, this is a quick reminder from Caltara.
            <Pause length="1"/>
            You have a past due balance of {amount} dollars, that was due on {due_date}.
            <Pause length="1"/>
            Please press 1 to speak with a representative to pay your balance now,
            or visit our website to make a payment today to avoid your current service from being interrupted.
        </Say>
    </Response>
    """
    call = client.calls.create(
        twiml=twiml,
        to=to,
        from_=TWILIO_PHONE
    )
    return call
