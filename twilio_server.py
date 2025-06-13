from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = FastAPI()

@app.get("/voice")
async def voice(name: str = "Customer", amount: str = "an unknown amount", due: str = "an unknown date"):
    response = VoiceResponse()
    gather = Gather(action="/process_input", method="POST", num_digits=1, timeout=5)
    gather.say(
        f"Hi {name}, this is a quick reminder from Caltara. "
        f"You have a past due balance of {amount} dollars, that was due on {due}. "
        "Please press 1 to speak with a representative to pay your balance now, "
        "or visit our website to make a payment today to avoid service interruption.",
        voice="Joanna"
    )
    response.append(gather)
    response.say("We did not receive any input. Goodbye!", voice="Joanna")
    return Response(content=str(response), media_type="text/xml")

@app.post("/process_input")
async def process_input(request: Request):
    form_data = await request.form()
    digits = form_data.get("Digits", "")
    response = VoiceResponse()

    if digits == "1":
        response.say("Please hold while we connect you to a representative.", voice="Joanna")
        response.dial("+1234567890")  # Replace with real number
    else:
        response.say("Invalid input. Goodbye!", voice="Joanna")

    return Response(content=str(response), media_type="text/xml")
