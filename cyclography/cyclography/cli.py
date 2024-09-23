
from cyclography.fetch import fetch_data
import argparse


def fetch_station_data():
    station_info = fetch_data("station_information.json")
    if station_info:
        print("Station Information:")
        for station in station_info['data']['stations']:
            print(f"Station Name: {station['name']}, Capacity: {station['capacity']}, "
                  f"Latitude: {station['lat']}, Longitude: {station['lon']}")
    else:
        print("Failed to fetch station information.")

def fetch_availability_data():
    station_status = fetch_data("station_status.json")
    if station_status:
        print("Station Availability:")
        for station in station_status['data']['stations']:
            print(f"Station ID: {station['station_id']}, Bikes Available: {station['num_bikes_available']}, "
                  f"Docks Available: {station['num_docks_available']}")
    else:
        print("Failed to fetch station availability.")


def main():
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
        fetch_station_data()
    elif args.availability:
        fetch_availability_data()
    elif args.both:
        fetch_station_data()
        print("\n")  # Line break
        fetch_availability_data()
    else:
        print("Please provide an option: --stations, --availability, or --both.")

# Entry point of the script
if __name__ == "__main__":
    main()