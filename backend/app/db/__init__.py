from app.db.database import MongoDB
from app.config import secrets
from app.db.crud import CRUD

mongodb = MongoDB(secrets.DATABASE_URL, secrets.MONGO_INITDB_DATABASE)
mongodb.connect()
SatellitesDB = mongodb.get_collection("satellites")
SatellitesDB.create_index("sat_id", unique=True)
LocationsDB = mongodb.get_collection("locations")

SatellitesCRUD = CRUD(
    SatellitesDB, cascaded_collection=LocationsDB, cascaded_field="sat_id"
)
LocationsCRUD = CRUD(
    LocationsDB, related_collection=SatellitesDB, reference_field="sat_id"
)
