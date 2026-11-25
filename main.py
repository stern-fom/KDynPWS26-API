import datetime

import fastapi
from fastapi import FastAPI
import typing
import uuid

app = FastAPI()

class RootResponse(typing.TypedDict):
    message: str


class DateResponse(typing.TypedDict):
    uuid: str
    title: str
    description: str
    start: datetime.datetime
    end: datetime.datetime


class NewDateRequest(typing.TypedDict):
    title: str
    description: typing.Optional[str]
    start: datetime.datetime
    end: datetime.datetime


sample_dates: list[DateResponse] = [
    DateResponse(
        uuid="1",
        title="Sample Event",
        description="This is a sample event",
        start=datetime.datetime(2026, 11, 20),
        end=datetime.datetime(2026, 11, 21)),
    DateResponse(
        uuid="2",
        title="Another Sample Event",
        description="This is another sample event",
        start=datetime.datetime(2026, 11, 22),
        end=datetime.datetime(2026, 11, 23)),
]

@app.get("/")
async def root() -> RootResponse:
    return {"message": "Hello World"}


@app.get("/dates")
async def get_dates() -> list[DateResponse]:
    return sample_dates

@app.get("/date/{uuid}")
async def get_date(uuid: str) -> DateResponse:
    for date in sample_dates:
        if date["uuid"] == uuid:
            return date
    raise fastapi.HTTPException(status_code=404, detail="Date not found")


@app.post("/date")
async def create_date(date: NewDateRequest) -> DateResponse:
    new_date = DateResponse(
        **date,
        uuid=str(uuid.uuid4())
    )
    sample_dates.append(new_date)
    return new_date


@app.delete("/date/{uuid}")
async def delete_date(uuid: str) -> DateResponse:
    for date in sample_dates:
        if date["uuid"] == uuid:
            sample_dates.remove(date)
            return date
    raise fastapi.HTTPException(status_code=404, detail="Date not found")


@app.put("/date/{uuid}")
async def update_date(uuid: str, date: NewDateRequest) -> DateResponse:
    for existing_date in sample_dates:
        if existing_date["uuid"] == uuid:
            existing_date.update(date)
            return existing_date
    raise fastapi.HTTPException(status_code=404, detail="Date not found")