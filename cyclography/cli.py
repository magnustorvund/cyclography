
from cyclography.fetch import fetch_data
from schemas import StationInfoResponse, StationStatusResponse  # Import the schemas
import argparse
import asyncio

async def fetch_station_data():
    station_info_response = await fetch_data("station_information.json", StationInfoResponse)
    if station_info_response:
        print("Station Information:")
        for station in station_info_response.data.stations:
            print(f"Station Name: {station.name}, Capacity: {station.capacity}, "
                  f"Latitude: {station.lat}, Longitude: {station.lon}")
    else:
        print("Failed to fetch station information.")

async def fetch_availability_data():
    station_status_response = await fetch_data("station_status.json", StationStatusResponse)
    if station_status_response:
        print("Station Availability:")
        for station in station_status_response.data.stations:
            print(f"Station ID: {station.station_id}, Bikes Available: {station.num_bikes_available}, "
                  f"Docks Available: {station.num_docks_available}")
    else:
        print("Failed to fetch station availability.")

async def fetch_and_combine_data():
    # Fetch station information
    station_info_response = await fetch_data("station_information.json", StationInfoResponse)
    if not station_info_response:
        print("Failed to fetch station information.")
        return None

    # Fetch station availability
    station_status_response = await fetch_data("station_status.json", StationStatusResponse)
    if not station_status_response:
        print("Failed to fetch station availability.")
        return None

    # Create a dictionary mapping station_id to station availability
    availability_dict = {
        station.station_id: station for station in station_status_response.data.stations
    }

    # Combine data
    combined_data = []
    for station_info in station_info_response.data.stations:
        station_id = station_info.station_id
        availability = availability_dict.get(station_id)
        if availability:
            combined_station = {
                "station_id": station_id,
                "name": station_info.name,
                "address": station_info.address,
                "capacity": station_info.capacity,
                "lat": station_info.lat,
                "lon": station_info.lon,
                "num_bikes_available": availability.num_bikes_available,
                "num_docks_available": availability.num_docks_available,
                "is_installed": bool(availability.is_installed),
                "is_renting": bool(availability.is_renting),
                "is_returning": bool(availability.is_returning),
            }
            combined_data.append(combined_station)
        else:
            print(f"Availability data not found for station ID {station_id}")

    return combined_data

def print_combined_station_data(combined_data):
    if combined_data:
        print("Combined Station Information and Availability:")
        for station in combined_data:
            print(f"Station ID: {station['station_id']}, Name: {station['name']}, "
                  f"Address: {station['address']}, Capacity: {station['capacity']}, "
                  f"Latitude: {station['lat']}, Longitude: {station['lon']}, "
                  f"Bikes Available: {station['num_bikes_available']}, "
                  f"Docks Available: {station['num_docks_available']}, "
                  f"Is Installed: {station['is_installed']}, "
                  f"Is Renting: {station['is_renting']}, "
                  f"Is Returning: {station['is_returning']}")
    else:
        print("No combined data to display.")

async def main():
    parser = argparse.ArgumentParser(description="Fetch Oslo Bysykkel station or availability data.")
    parser.add_argument(
        '--stations',
        action='store_true',
        help="Fetch station information data"
    )
    parser.add_argument(
        '--availability',
        action='store_true',
        help="Fetch station availability data"
    )
    parser.add_argument(
        '--both',
        action='store_true',
        help="Fetch both station and availability data"
    )

    args = parser.parse_args()

    if args.stations:
        await fetch_station_data()
    elif args.availability:
        await fetch_availability_data()
    elif args.both:
        combined_data = await fetch_and_combine_data()
        print_combined_station_data(combined_data)
    else:
        print("Please provide an option: --stations, --availability, or --both.")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())