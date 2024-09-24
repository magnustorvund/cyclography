from pydantic import BaseModel
from typing import List, Optional


class StationStatus(BaseModel):
    station_id: str
    is_installed: int  # API returns 1 or 0
    is_renting: int    # API returns 1 or 0
    is_returning: int  # API returns 1 or 0
    last_reported: int
    num_bikes_available: int
    num_docks_available: int

class StationStatusData(BaseModel):
    stations: List[StationStatus]

class StationStatusResponse(BaseModel):
    last_updated: int
    data: StationStatusData

class DockAvailabilityResponse(BaseModel):
    station_id: str
    num_bikes_available: int
    num_docks_available: int
    is_installed: bool  # We'll convert the integer to boolean
    is_renting: bool    # We'll convert the integer to boolean
    is_returning: bool  # We'll convert the integer to boolean

class StationInfo(BaseModel):
    station_id: str
    name: str
    address: str
    lat: float
    lon: float
    capacity: int

class StationInfoData(BaseModel):
    stations: List[StationInfo]

class StationInfoResponse(BaseModel):
    last_updated: int
    data: StationInfoData

class ClosestStationResponse(BaseModel):
    station_id: str
    name: str
    address: str
    lat: float
    lon: float
    distance_in_meters: float
