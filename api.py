from typing import Union
import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"name": "speeed"}


@app.get("/locations")
def read_locations():
    locations = []
    try:
        with open('locations.json') as f:
            d = json.load(f)
            return d
    except Exception as e:
        print("Error while opening locations.json file: " + e)
        return locations