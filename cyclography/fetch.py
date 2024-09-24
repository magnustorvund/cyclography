from fastapi import HTTPException

import requests
from pydantic import BaseModel, ValidationError

client_identifier = "magnustorvund-cyclography"
base_url = "https://gbfs.urbansharing.com/oslobysykkel.no/"

headers = {
    "Client-Identifier": client_identifier
}

# Function to fetch data from an endpoint and validate it with a Pydantic model
async def fetch_data(endpoint: str, schema: BaseModel) -> dict[any]:
    url = base_url + endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            # Validate the response using the Pydantic schema
            validated_data = schema.model_validate(response.json())
            return validated_data
        except ValidationError as e:
            # Handle validation errors
            raise HTTPException(status_code=422, detail=f"Validation error: {e}")
