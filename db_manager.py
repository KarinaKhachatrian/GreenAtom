import psycopg2
from parse import (flight_ids, flight_callsigns, flight_icaos, airlines, aircraft_codes,
                   origin_airports, destination_airports, aircrafts_speed, flights_altitude, flights_latitude, flight_longitude)
from datetime import datetime

def create_tables(conn, cursor):
    try:
        callsign_table = cursor.execute("""CREATE TABLE IF NOT EXISTS CallSign(
                                        CallSignID SERIAL PRIMARY KEY,
                                        CallSignName TEXT);""")

        aircraft_table = cursor.execute("""CREATE TABLE IF NOT EXISTS Aircraft(
                                        AircraftID SERIAL PRIMARY KEY,
                                        AircraftName TEXT);""")

        origin_airport_table = cursor.execute("""CREATE TABLE IF NOT EXISTS OriginAirport(
                                        OriginAirportID SERIAL PRIMARY KEY,
                                        OriginAirportName TEXT);""")

        destination_airport_table = cursor.execute("""CREATE TABLE IF NOT EXISTS DestinationAirport(
                                        DestinationAirportID SERIAL PRIMARY KEY,
                                        DestinationAirportName TEXT);""")

        icao_table = cursor.execute("""CREATE TABLE IF NOT EXISTS ICAO(
                                        ICAOID SERIAL PRIMARY KEY,
                                        CodeICAO TEXT);""")

        airline_table = cursor.execute("""CREATE TABLE IF NOT EXISTS Airline(
                                        AirlineID SERIAL PRIMARY KEY,
                                        AirlineName TEXT);""")

        flight_table = cursor.execute("""CREATE TABLE IF NOT EXISTS Flight(
                                        FlightID TEXT UNIQUE PRIMARY KEY,
                                        CallSignID INT REFERENCES CallSign (CallSignID),
                                        ICAOID INT REFERENCES ICAO (ICAOID),
                                        AirlineID INT REFERENCES Airline (AirlineID),
                                        OriginAirportID INT REFERENCES OriginAirport (OriginAirportID),
                                        DestinationAirportID INT REFERENCES DestinationAirport (DestinationAirportID),
                                        AircraftID INT REFERENCES Aircraft (AircraftID),
                                        AircraftSpeed INT,
                                        Altitude REAL,
                                        Latitude REAL,
                                        Longitude REAL,
                                        Timestamp TIMESTAMP);""")

        conn.commit()
        return "Таблицы созданы.\n"

    except Exception as e:
        return f"Ошибка {Exception.__class__.__name__}\n{e}"

def insert_tables(conn, cursor):
    try:
        for callsign in flight_callsigns:
            cursor.execute("""INSERT INTO CallSign (CallSignName) VALUES (%s)""", (callsign,))

        for origin_airport in origin_airports:
            cursor.execute("""INSERT INTO OriginAirport (OriginAirportName) VALUES (%s)""", (origin_airport,))

        for destination_airport in destination_airports:
            cursor.execute("""INSERT INTO DestinationAirport (DestinationAirportName) VALUES (%s)""", (destination_airport,))

        for icao in flight_icaos:
            cursor.execute("""INSERT INTO ICAO (CodeICAO) VALUES (%s)""", (icao,))

        for airline in airlines:
            cursor.execute("""INSERT INTO Airline (AirlineName) VALUES (%s)""", (airline,))

        for aircraft in aircraft_codes:
            cursor.execute("""INSERT INTO Aircraft (AircraftName) VALUES (%s)""", (aircraft,))

        conn.commit()
        return "Промежуточные данные успешно добавлены.\n"

    except Exception as e:
        return f"Ошибка {type(e).__name__}\n{e}"

def clear_tables(conn, cursor):
    try:
        cursor.execute("TRUNCATE TABLE Flight RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE CallSign RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE ICAO RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE Airline RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE OriginAirport RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE DestinationAirport RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE Aircraft RESTART IDENTITY CASCADE;")
        conn.commit()
        return "Все таблицы очищены.\n"
    except Exception as e:
        return f"Ошибка при очистке: {type(e).__name__}\n{e}"

def get_id(cursor, table, column, value):
    cursor.execute(f"SELECT {table}ID FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_flights(conn, cursor):
    now = datetime.now()
    try:
        for i in range(len(flight_ids)):
            call_sign_id = get_id(cursor, "CallSign", "CallSignName", flight_callsigns[i])
            icao_id = get_id(cursor, "ICAO", "CodeICAO", flight_icaos[i])
            airline_id = get_id(cursor, "Airline", "AirlineName", airlines[i])
            origin_id = get_id(cursor, "OriginAirport", "OriginAirportName", origin_airports[i])
            destination_id = get_id(cursor, "DestinationAirport", "DestinationAirportName", destination_airports[i])
            aircraft_id = get_id(cursor, "Aircraft", "AircraftName", aircraft_codes[i])
            speed = aircrafts_speed[i]
            altitude = flights_altitude[i]
            latitude = flights_latitude[i]
            longitude = flight_longitude[i]

            cursor.execute("""
                INSERT INTO Flight (
                    FlightID, CallSignID, ICAOID, AirlineID, OriginAirportID, DestinationAirportID,
                    AircraftID, AircraftSpeed, Altitude, Latitude, Longitude, Timestamp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                flight_ids[i], call_sign_id, icao_id, airline_id, origin_id, destination_id,
                aircraft_id, speed, altitude, latitude, longitude, now
            ))

        conn.commit()
        return "Полеты успешно заполнены.\n"

    except Exception as e:
        return f"Ошибка {type(e).__name__}\n{e}"

conn = psycopg2.connect(dbname="flydb", user="postgres",
                                password="postgres", host="db")
cursor = conn.cursor()
print(create_tables(conn, cursor))
print(clear_tables(conn, cursor))
print(insert_tables(conn, cursor))
print(insert_flights(conn, cursor))