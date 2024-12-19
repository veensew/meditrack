import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    # MongoDB Configuration
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'meditrack')

    # Redshift Configuration
    REDSHIFT_CONFIG = {
        'dbname': os.getenv('REDSHIFT_DB', 'meditrack'),
        'host': os.getenv('REDSHIFT_HOST'),
        'port': int(os.getenv('REDSHIFT_PORT', '5439')),
        'user': os.getenv('REDSHIFT_USER'),
        'password': os.getenv('REDSHIFT_PASSWORD')
    }