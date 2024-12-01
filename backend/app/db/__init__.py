from app.db.database import MongoDB
from app.config import secrets
from app.db.crud import CRUD

# Initialization and connection to the database using the MongoDB Class
mongodb = MongoDB(secrets.DATABASE_URL, secrets.MONGO_INITDB_DATABASE)
mongodb.connect()
# Creation of the required collections
SatellitesDB = mongodb.get_collection("satellites")
# Mark sat_id as unique in the Satellites collection
SatellitesDB.create_index("sat_id", unique=True)
LocationsDB = mongodb.get_collection("locations")

# Prepare the CRUD classes for each collection with the required relationships
# When a Satellite is changed then this cascades to the LocationsDB because of sat_id
SatellitesCRUD = CRUD(
    SatellitesDB, cascaded_collection=LocationsDB, cascaded_field="sat_id"
)
# When a Locations is created or updated then sat_id needs to exist in the SatellitesDB
LocationsCRUD = CRUD(
    LocationsDB, related_collection=SatellitesDB, reference_field="sat_id"
)
