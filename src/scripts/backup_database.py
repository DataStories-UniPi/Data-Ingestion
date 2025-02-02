import csv
import time
from datetime import datetime

import config as cfg
import schedule
from database import make_connection


# Function to create a backup of a table to a CSV file
def backup_table_to_csv(table_name):
    try:
        engine = make_connection()
        with engine.connect() as conn:

            cursor = engine.raw_connection().cursor()
            # Fetch data from the table
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Get column names
            column_names = [desc[0] for desc in cursor.description]

            # Generate a timestamp for the backup file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = cfg.BACKUP_DIR / f"{table_name}_backup_{timestamp}.csv"

            # Write data to CSV file
            with open(backup_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  # Write header
                writer.writerows(rows)  # Write rows

        print(f"Backup of table '{table_name}' completed successfully. File: {backup_file}")

    except Exception as e:
        print(f"Error during backup of table '{table_name}': {e}")

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()


def backup_database():
    try:
        engine = make_connection()
        with engine.connect() as conn:

            cursor = engine.raw_connection().cursor()

            # Get list of all tables in the database
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """
            )
            tables = cursor.fetchall()

            # Backup each table
            for table in tables:
                table_name = table[0]
                backup_table_to_csv(table_name)

    except Exception as e:
        print(f"Error during database backup: {e}")

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()


# Schedule the backup task
schedule.every(cfg.BACKUP_INTERVAL).hours.do(backup_database)

# Main loop to keep the script running
if __name__ == "__main__":
    print(f"Starting PostgreSQL backup. Backups will run every {cfg.BACKUP_INTERVAL} hour(s).")
    while True:
        schedule.run_pending()
        time.sleep(1)
