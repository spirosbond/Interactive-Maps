from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.db
from app.routers import satellites, locations, iss
from app.config import app_config
from app.services.task_scheduler import TaskScheduler

# Initialize FastAPI application with the provided configuration
app = FastAPI(
    title=app_config.app_title,
    description=app_config.app_description,
    summary=app_config.app_summary,
    version=app_config.app_version,
    terms_of_service=app_config.app_terms_of_service,
)
# Initialize the task scheduler
taskScheduler = TaskScheduler()


# Start the task scheduler when application starts
@app.on_event("startup")
async def start_scheduler():
    taskScheduler.start()


# Stop the task scheduler when application starts
@app.on_event("shutdown")
async def stop_scheduler():
    taskScheduler.stop()


# To allow localhost:3000 to connect. Normally for production this should be removed and replaced with the actual origins.
# Alternatively, hosting the backed and the front end in Google Cloud you can restrict connections through a VPC
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import all routers
app.include_router(satellites.router, tags=["Satellite"], prefix="/api/satellite")
app.include_router(locations.router, tags=["Location"], prefix="/api/location")
app.include_router(iss.router, tags=["ISS"], prefix="/api/iss")


# Dummy router to healthcheck the API
@app.get("/api/healthchecker", tags=["Generic"])
def healthchecker():
    return {"message": "Welcome to Interactive Maps API"}
