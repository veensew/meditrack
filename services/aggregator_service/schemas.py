REDSHIFT_SCHEMAS = {
    'doctor_appointments': """
        CREATE TABLE IF NOT EXISTS doctor_appointments (
            doctor_id VARCHAR(255),
            doctor_name VARCHAR(255),
            specialty VARCHAR(255),
            appointment_count INTEGER,
            aggregation_date DATE,
            PRIMARY KEY (doctor_id, aggregation_date)
        )
    """,
    'appointment_frequency': """
        CREATE TABLE IF NOT EXISTS appointment_frequency (
            date DATE,
            appointment_count INTEGER,
            aggregation_date DATE,
            PRIMARY KEY (date, aggregation_date)
        )
    """,
    'symptoms_specialty': """
        CREATE TABLE IF NOT EXISTS symptoms_by_specialty (
            specialty VARCHAR(255),
            symptom VARCHAR(255),
            occurrence_count INTEGER,
            aggregation_date DATE,
            PRIMARY KEY (specialty, symptom, aggregation_date)
        )
    """
}