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

def def send_voice(to, name, amount, due_date):
    twiml = f"""
    <Response>
        <Gather numDigits="1" action="/handle-key" method="POST" timeout="6">
            <Say voice="alice" language="en-US">
                Hello {name}, this is Caltara with a courtesy reminder.
                <Pause length="1"/>
                Our records show an outstanding balance of {amount} dollars,
                due on {due_date}.
                <Pause length="1"/>
                If you would like to speak with someone now regarding your past due balance, please press 1.
                <Pause length="1"/>
                Or, you can take care of this online at your convenience.
                <Pause length="1"/>
                We appreciate your attention to this matter.
            </Say>
        </Gather>
        <Say voice="alice" language="en-US">
            We didn’t receive any input. Please feel free to reach out with any questions.
            Goodbye for now.
        </Say>
    </Response>
    """
    call = client.calls.create(
        twiml=twiml,
        to=to,
        from_=TWILIO_PHONE
    )
    return call
