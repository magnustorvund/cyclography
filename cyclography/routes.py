from fastapi import HTTPException
from geopy.distance import geodesic
from cyclography.fetch import fetch_data
from cyclography.schemas import DockAvailabilityResponse, StationInfoResponse, StationStatusResponse, ClosestStationResponse
from cyclography.main import app

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Endpoint 1: Check if there's dock availability at a given station
@app.get("/check-dock-availability/{station_id}", response_model=DockAvailabilityResponse)
async def get_dock_availability(station_id: str):
    # Fetch and validate station status data
    station_status = await fetch_data("station_status.json", StationStatusResponse)
    if station_status is None:
        raise HTTPException(status_code=500, detail="Could not fetch station status data")

    # Find the specific station
    for station in station_status['data']['stations']:
        if station['station_id'] == station_id:
            return DockAvailabilityResponse(
                station_id=station['station_id'],
                num_docks_availablesss=station['num_docks_available'],
                is_renting=station['is_renting'],
                is_installed=station['is_installed'],
                is_returning=station['is_returning']
            )

    raise HTTPException(status_code=404, detail="Station not found")

# Endpoint 2: Find the closest station based on latitude and longitude
@app.get("/closest-station/", response_model=ClosestStationResponse)
async def get_closest_station(lat: float, lon: float):
    # Fetch and validate station information data
    station_info = await fetch_data("station_information.json", StationInfoResponse)
    if station_info is None:
        raise HTTPException(status_code=500, detail="Could not fetch station information data")

    closest = None
    min_distance = float('inf')

    current_location = (lat, lon)

    # Find the closest station based on geolocation
    for station in station_info['data']['stations']:
        station_location = (station['lat'], station['lon'])
        distance = geodesic(current_location, station_location).meters  # Calculate distance in meters

        if distance < min_distance:
            min_distance = distance
            closest = station

    if closest:
        return ClosestStationResponse(
            station_id=closest['station_id'],
            name=closest['name'],
            address=closest['address'],
            lat=closest['lat'],
            lon=closest['lon'],
            distance_in_meters=min_distance
        )

    raise HTTPException(status_code=404, detail="No stations found")
