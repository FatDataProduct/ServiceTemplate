from pydantic import BaseModel, validator
from datetime import datetime, timedelta, timezone
from typing import Optinal

class ParsingDates(BaseModel):
    start_date: Optinal[datetime] = datetime.now(timezone.utc) - timedelta(days=10)
    end_date: Optinal[datetime] = datetime.now(timezone.utc)

    @validator("start_date", "end_date", pre=True)
    def set_timezone(cls, value):
        if isinstance(value, str):
            value = datetime.fromisoformat(value.rstrip("Z"))

        value = value.replace(tzinfo=timezone.utc)
        return value
