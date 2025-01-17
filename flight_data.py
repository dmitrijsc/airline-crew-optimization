import requests
import pytz
from datetime import datetime, timedelta

class Flight:
    def __init__(self, orig, dest, depart, arrival, flight_number, duration):
        self.orig = orig
        self.dest = dest
        self.depart = depart
        self.arrival = arrival
        self.flight_number = flight_number
        self.duration = duration

    def get_id(self):
        return self.flight_number

class FlightData:
    def __init__(self, base_airports):
        self.base_airports = base_airports
        self.flights = []

    def parse_datetime(self, dt_string):
        # Parse the datetime string
        dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M%z")
        # Convert to UTC
        return dt.astimezone(pytz.UTC)

    def calculate_duration(self, depart_time, arrival_time):
        # Calculate the time difference
        time_difference = arrival_time - depart_time
        # Convert to minutes
        return int(time_difference.total_seconds() / 60)

    def read_flights(self):
        for base_airport in self.base_airports:
            self.read_route_flights(f'https://api.airbaltic.com/schedule/live/orig/{base_airport}')

    def read_route_flights(self, url):
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            for flight_date in data:

                for leg in data[flight_date]:

                    leg = leg['legs'][0]

                    # Parse depart and arrival times
                    depart_time = self.parse_datetime(leg['depart'])
                    arrival_time = self.parse_datetime(leg['arrival'])

                    # Calculate the duration of the flight
                    duration = self.calculate_duration(depart_time, arrival_time)

                    flight = Flight(
                        orig=leg['orig'],
                        dest=leg['dest'],
                        depart=depart_time,
                        arrival=arrival_time,
                        flight_number=leg['flightNumber'],
                        duration=duration
                    )

                    self.flights.append(flight)

                    # since we do not query for all flights, we assume the plane an hour later will return
                    # add the same flight to a departure airport, adjust departure and arrival times by 
                    # assuming it will depart an hour after the first flight arrival
                    return_flight = Flight(
                        orig=leg['dest'],
                        dest=leg['orig'],
                        depart=arrival_time + timedelta(hours=1),
                        arrival=arrival_time + timedelta(hours=1) + timedelta(minutes=duration),
                        flight_number=leg['flightNumber'] + 'R',
                        duration=duration
                    )

                    self.flights.append(return_flight)
            
                # sort flights by departure time asc
                # Remove duplicates based on flight_number, orig, and depart
                self.flights.sort(key=lambda x: x.depart)

                unique_flights = {}
                for flight in self.flights:
                    key = (flight.flight_number, flight.orig, flight.depart)
                    if key not in unique_flights:
                        unique_flights[key] = flight

                # Update self.flights with unique flights and sort by departure time
                self.flights = list(unique_flights.values())

                    
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")

