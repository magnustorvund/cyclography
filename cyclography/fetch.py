from fastapi import HTTPException
import requests
from pydantic import BaseModel, ValidationError
from typing import Any, Type

client_identifier = "magnustorvund-cyclography"
base_url = "https://gbfs.urbansharing.com/oslobysykkel.no/"

headers = {
    "Client-Identifier": client_identifier
}

async def fetch_data(endpoint: str, schema: Type[BaseModel]) -> BaseModel:
    url = base_url + endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            # Validate the response using the Pydantic schema
            validated_data = schema(**response.json())
            return validated_data
        except ValidationError as e:
            # Handle validation errors
            raise HTTPException(status_code=422, detail=f"Validation error: {e}")
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch data from the API."
        )
