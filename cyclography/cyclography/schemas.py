from pydantic import BaseModel
from typing import List, Optional


class StationStatus(BaseModel):
    station_id: str
    num_bikes_available: int
    num_docks_available: int
    is_renting: bool
    is_installed: bool
    is_returning: bool
    last_reported: int

class StationStatusResponse(BaseModel):
    data: dict
    stations: List[StationStatus]

class StationInfo(BaseModel):
    station_id: str
    name: str
    address: str
    lat: float
    lon: float
    capacity: int

class StationInfoResponse(BaseModel):
    data: dict
    stations: List[StationInfo]

class DockAvailabilityResponse(BaseModel):
    station_id: str
    num_docks_available: int
    is_renting: bool
    is_installed: bool
    is_returning: bool

class ClosestStationResponse(BaseModel):
    station_id: str
    name: str
    address: str
    lat: float
    lon: float
    distance_in_meters: float