import requests
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from typing import Type

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
            validated_data = schema.model_validate(response.json())
            return validated_data
        except ValidationError as e:
            # Handle validation errors
            raise HTTPException(status_code=422, detail=f"Validation error: {e}")
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch data from the API."
        )
