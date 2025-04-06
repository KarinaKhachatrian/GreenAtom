import pandas as pd
from db_manager import conn

query = """
SELECT
    c.CallSignName as Call_Sign,
    i.CodeICAO as ICAO_code,
    a.AircraftName AS Aircraft_Model,
    al.AirlineName AS Airline,
    f.Altitude AS Altitude,
    f.Latitude AS Latitude,
    f.Longitude AS Longitude,
    DATE(f.Timestamp) AS Flight_Date,
    COUNT(*) AS Flight_Count
FROM
    Flight f
JOIN Aircraft a ON f.AircraftID = a.AircraftID
JOIN Airline al ON f.AirlineID = al.AirlineID
JOIN CallSign c ON f.CallSignID = c.CallSignID
JOIN ICAO i ON f.ICAOID = i.ICAOID
WHERE
    f.Timestamp >= NOW() - INTERVAL '1 day'
GROUP BY
    c.CallSignName, i.CodeICAO, a.AircraftName, al.AirlineName, f.Altitude, f.Latitude, f.Longitude, DATE(f.Timestamp)
ORDER BY
    Flight_Count DESC;
"""

df = pd.read_sql(query, conn)
df.index = df.index + 1
df.to_csv("flight.csv", index=True)