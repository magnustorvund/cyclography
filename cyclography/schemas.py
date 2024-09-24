from pydantic import BaseModel
from typing import List, Optional


class StationStatus(BaseModel):
    station_id: str
    is_installed: int
    is_renting: int
    is_returning: int
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
    is_installed: bool
    is_renting: bool
    is_returning: bool

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
