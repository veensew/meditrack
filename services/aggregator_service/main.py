from database import DatabaseConnection
from aggregators import DataAggregators
from schemas import REDSHIFT_SCHEMAS
from datetime import datetime
from config import logger
from typing import List, Dict, Any

class DataAggregatorService:
    def __init__(self):
        self.db_conn = DatabaseConnection()
        self.mongo_db = self.db_conn.get_mongo_client()
        self.aggregators = DataAggregators(self.mongo_db)

    def initialize_redshift_tables(self):
        """Initialize Redshift tables if they don't exist"""
        with self.db_conn.get_redshift_cursor() as cursor:
            for schema in REDSHIFT_SCHEMAS.values():
                cursor.execute(schema)

    def save_to_redshift(self, data: List[Dict], table_name: str, columns: List[str]):
        """Save aggregated data to Redshift"""
        if not data:
            logger.warning(f"No data to save for table {table_name}")
            return

        values_template = "(" + ",".join(["%s"] * len(columns)) + ")"
        query = f"""
            INSERT INTO {table_name} 
            ({','.join(columns)}) 
            VALUES {values_template}
        """

        with self.db_conn.get_redshift_cursor() as cursor:
            for item in data:
                values = [item[col] for col in columns[:-1]]
                values.append(datetime.now().date())
                cursor.execute(query, values)

    def run_aggregation(self):
        """Run all aggregations and save to Redshift"""
        try:
            logger.info("Starting data aggregation")

            # Initialize Redshift tables
            self.initialize_redshift_tables()

            # Aggregate and save doctor appointments
            doctor_appointments = self.aggregators.aggregate_doctor_appointments()
            self.save_to_redshift(
                doctor_appointments,
                "doctor_appointments",
                ["doctor_id", "doctor_name", "specialty", "appointment_count", "aggregation_date"]
            )

            # Aggregate and save appointment frequency
            appointment_freq = self.aggregators.aggregate_appointment_frequency()
            self.save_to_redshift(
                appointment_freq,
                "appointment_frequency",
                ["date", "appointment_count", "aggregation_date"]
            )

            # Aggregate and save symptoms by specialty
            symptoms_specialty = self.aggregators.aggregate_symptoms_by_specialty()
            self.save_to_redshift(
                symptoms_specialty,
                "symptoms_by_specialty",
                ["specialty", "symptom", "occurrence_count", "aggregation_date"]
            )

            logger.info("Data aggregation completed successfully")

        except Exception as e:
            logger.error(f"Error during aggregation process: {str(e)}")
            raise

if __name__ == "__main__":
    aggregator = DataAggregatorService()
    aggregator.run_aggregation()
