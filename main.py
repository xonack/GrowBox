from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime;
import os

app = FastAPI()


#TODO: expose app port to prometheus

class State(BaseModel):
    timestamp: str = ""
    soil_humidity: str = ""
    air_humidity: str = ""
    temperature: str = ""
    water_resrve: str = ""

last_state = State()

@app.get("/hello")
def hello_view(name: str = "Jens"):
    return {
        "message": f'Hello there, {name}!'
    }


# curl -H "Content-Type: application/json" --request POST --data '{"timestamp": "1618270370.13393", "soil_humidity": "-1", "air_humidity": "-2", "temperature": "-3", "water_reserve": "-4"}' http://localhost:9090/state

@app.post("/state")
def add_bender(state: State):

    if (not state) :
        raise HTTPException(status_code=400, detail="state missing!")


    last_state = state

    return {
        "message": f"Set state at {last_state.timestamp}; temp = {last_state.temperature}!",
    }



@app.get("/time")
def get_time():

    current_time = datetime.datetime.now()

    timestamp = current_time.timestamp()

    return {
        "timestamp": timestamp,
        "current_time": current_time
    }
