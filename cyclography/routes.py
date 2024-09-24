from fastapi import APIRouter, HTTPException
from geopy.distance import geodesic
from typing import Dict
from fetch import fetch_data
from schemas import (
    DockAvailabilityResponse,
    StationStatusResponse,
    ClosestStationResponse,
    StationInfoResponse,
    StationStatus
)

router = APIRouter()

@router.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Cyclography API!"}


@router.get("/check-dock-availability/{station_id}", response_model=DockAvailabilityResponse)
async def get_dock_availability(station_id: str):
    """Get dock availability data for a given station id."""

    station_status_response = await fetch_data("station_status.json", StationStatusResponse)
    if station_status_response is None:
        raise HTTPException(status_code=500, detail="Could not fetch station status data")

    # Convert the list of stations to a dictionary for O(1) access
    station_dict: Dict[str, StationStatus] = {
        station.station_id: station for station in station_status_response.data.stations
    }

    station = station_dict.get(station_id)
    if station:
        return DockAvailabilityResponse(
            station_id=station.station_id,
            num_bikes_available=station.num_bikes_available,
            num_docks_available=station.num_docks_available,
            is_installed=bool(station.is_installed),
            is_renting=bool(station.is_renting),
            is_returning=bool(station.is_returning)
        )

    raise HTTPException(status_code=404, detail="Station not found")


@router.get("/closest-station/", response_model=ClosestStationResponse)
async def get_closest_station(lat: float, lon: float):
    """Find the closest station based on latitude and longitude."""

    station_info_response = await fetch_data("station_information.json", StationInfoResponse)
    if station_info_response is None:
        raise HTTPException(status_code=500, detail="Could not fetch station information data")

    closest_station = None
    min_distance = float('inf')

    current_location = (lat, lon)

    # Access stations correctly
    for station in station_info_response.data.stations:
        station_location = (station.lat, station.lon)
        distance = geodesic(current_location, station_location).meters  # Calculate distance in meters

        if distance < min_distance:
            min_distance = distance
            closest_station = station

    if closest_station:
        return ClosestStationResponse(
            station_id=closest_station.station_id,
            name=closest_station.name,
            address=closest_station.address,
            lat=closest_station.lat,
            lon=closest_station.lon,
            distance_in_meters=min_distance
        )

    raise HTTPException(status_code=404, detail="No stations found")