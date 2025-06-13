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
    twiml = f"<Response><Say>Hi {name}, this is a payment reminder from Caltara. You have an outstanding invoice of {amount} dollars, due on {due_date}. Please press 1 to talk to a representative or visit your invoice link.</Say></Response>"
    call = client.calls.create(
        twiml=twiml,
        to=to,
        from_=TWILIO_PHONE
    )
    return call
