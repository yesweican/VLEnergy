import logging
import azure.functions as func
import json
import pyodbc
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Data injection function started.")

    try:
        # Read JSON body
        data = req.get_json()

        client_id = data.get("Client_ID")
        device_id = data.get("Device_ID")
        device_reading = data.get("Device_Reading")
        reading_unit = data.get("Reading_Unit")
        timestamp = data.get("TimeStamp")

        # Validate required fields
        missing = [
            key for key, value in {
                "Client_ID": client_id,
                "Device_ID": device_id,
                "Device_Reading": device_reading,
                "Reading_Unit": reading_unit,
                "TimeStamp": timestamp
            }.items() if value is None
        ]

        if missing:
            return func.HttpResponse(
                f"Missing required fields: {', '.join(missing)}", status_code=400
            )

        # Get SQL connection string from environment
        conn_str = os.getenv("SQL_CONNECTION_STRING")
        if not conn_str:
            return func.HttpResponse(
                "Missing SQL_CONNECTION_STRING in Function App Settings.",
                status_code=500
            )

        # Connect to Azure SQL
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insert SQL row
        insert_query = """
            INSERT INTO Raw_Data (Client_ID, Device_ID, Device_Reading, Reading_Unit, TimeStamp)
            VALUES (?, ?, ?, ?, ?)
        """

        cursor.execute(
            insert_query,
            client_id,
            device_id,
            float(device_reading),
            reading_unit,
            timestamp
        )

        conn.commit()
        cursor.close()
        conn.close()

        return func.HttpResponse("Data inserted successfully.", status_code=200)

    except ValueError:
        return func.HttpResponse("Invalid JSON body.", status_code=400)

    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        return func.HttpResponse(
            f"Server error: {str(e)}", status_code=500
        )
