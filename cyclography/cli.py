
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
        await fetch_station_data()
        print("\n")  # Line break
        await fetch_availability_data()
    else:
        print("Please provide an option: --stations, --availability, or --both.")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())