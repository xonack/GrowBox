from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime;
import os

app = FastAPI()


#Prometheus --------------------------------------------------------------------

from prometheus_fastapi_instrumentator import Instrumentator, metrics
from typing import Callable
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Counter, Gauge

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    # should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    # env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)

def http_temperature() -> Callable[[Info], None]:
    TEMPERATURE = Gauge(
        "http_temperature",
        "Current temperature.",
    )

    def instrumentation(info: Info) -> None:
        print("Request: ")
        print(info.request)
        print("url: ")
        print(info.request.url)
        # if info.request.headers["temp"]:
        #     temp = info.request.headers["temp"]
        #     TEMPERATURE.set(temp)
        TEMPERATURE.set(last_temp)

    return instrumentation

instrumentator.add(http_temperature())
#
# def http_humidity() -> Callable[[Info], None]:
#     HUMIDITY = Gauge(
#         "http_humidity",
#         "Current humidity.",
#     )
#
#     def instrumentation(info: Info) -> None:
#         humidity = info.request.headers["humidity"]
#         HUMIDITY.set(humidity)
#
#     return instrumentation
#
# instrumentator.add(http_humidity())

instrumentator.instrument(app)

instrumentator.expose(app, include_in_schema=False, should_gzip=True)

# ------------------------------------------------------------------------------

#TODO: expose app port to prometheus

class State(BaseModel):
    temp: int = ""
    air_humidity: int = ""
    water_level: int = ""

last_state = State()

last_ts = -1
last_temp = -1
last_air_humidity = -1
last_water_level = -1

@app.get("/")
def hello_view():
    return {
        "message": f'Connected!'
    }

@app.get("/hello")
def hello_view(name: str = "Jens"):
    return {
        "message": f'Hello there, {name}!'
    }


# curl -H "Content-Type: application/json" --request POST --data '{"timestamp": "1618270370.13393", "soil_humidity": "-1", "air_humidity": "-2", "temperature": "-3", "water_level": "-4"}' http://localhost:9090/state

@app.post("/state")
# def add_bender(temp: int, air_humidity: int, water_level: int):
#
#     if (not temp) :
#         raise HTTPException(status_code=400, detail="temp missing!")
#
#     if (not air_humidity) :
#         raise HTTPException(status_code=400, detail="air_humidity missing!")
#
#     if (not water_level) :
#         raise HTTPException(status_code=400, detail="water_level missing!")
    # current_time = datetime.datetime.now()
    # last_ts = current_time.timestamp()
    # last_temp = temp
    # last_air_humidity = air_humidity
    # last_water_level = water_level

def add_bender(state: State):

    if (not state) :
        raise HTTPException(status_code=400, detail="state missing!")



    current_time = datetime.datetime.now()
    last_ts = current_time.timestamp()
    last_temp = state.temp
    last_air_humidity = state.air_humidity
    last_water_level = state.water_level

    return {
        "message": f"Set state at {last_ts}; temp = {last_temp}, air_humidity = {last_air_humidity}, water_level = {last_water_level}",
    }

@app.post("/temperature")
def add_bender(temperature: int):

    if (not temperature) :
        raise HTTPException(status_code=400, detail="temperature missing!")


    last_state.temperature = temperature

    return {
        "message": f"Set temperature at temp = {temperature}!",
    }



@app.get("/time")
def get_time():

    current_time = datetime.datetime.now()

    timestamp = current_time.timestamp()

    return {
        "timestamp": timestamp,
        "current_time": current_time
    }
