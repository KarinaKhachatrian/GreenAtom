from FlightRadar24 import FlightRadar24API

api = FlightRadar24API()

bounds = "47.5,27.0,40.5,42.5"

flights = api.get_flights(bounds=bounds)
print(f"Найдено {len(flights)} рейсов в акватории Чёрного моря.\n")
flight_ids = []
flight_callsigns = []
flight_icaos = []
aircraft_codes = []
airlines = []
origin_airports = []
destination_airports = []
aircrafts_speed = []
flights_altitude = []
flights_latitude = []
flight_longitude = []

for flight in flights:

    flight_ids.append(flight.id)
    flight_callsigns.append(flight.callsign)
    flight_icaos.append(flight.airline_icao)
    aircraft_codes.append(flight.aircraft_code)
    origin_airports.append(flight.origin_airport_iata)
    destination_airports.append(flight.destination_airport_iata)
    aircrafts_speed.append(flight.ground_speed)
    flights_altitude.append(flight.altitude)
    flights_latitude.append(flight.latitude)
    flight_longitude.append(flight.longitude)
    airlines.append(flight.airline_iata)