# from app.routers import note
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# from fastapi.middleware.cors import CORSMiddleware

# from src.routers import episode, user, channel, kpi, admin
import app.db
from app.routers import satellites, locations, iss
from app.config import app_config
from app.services.task_scheduler import TaskScheduler

app = FastAPI(
    title=app_config.app_title,
    description=app_config.app_description,
    summary=app_config.app_summary,
    version=app_config.app_version,
    terms_of_service=app_config.app_terms_of_service,
)
taskScheduler = TaskScheduler()


@app.on_event("startup")
async def start_scheduler():
    taskScheduler.start()


@app.on_event("shutdown")
async def stop_scheduler():
    taskScheduler.stop()


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


# app.include_router(note.router, tags=['Notes'], prefix='/api/notes')
# app.include_router(user.router, tags=["User"], prefix="/api/user")
# app.include_router(channel.router, tags=["Channel"], prefix="/api/channel")
app.include_router(satellites.router, tags=["Satellite"], prefix="/api/satellite")
app.include_router(locations.router, tags=["Location"], prefix="/api/location")
app.include_router(iss.router, tags=["ISS"], prefix="/api/iss")
# app.include_router(kpi.router, tags=["KPI"], prefix="/api/kpi")
# app.include_router(admin.router, tags=["Admin"], prefix="/api/admin")


@app.get("/api/healthchecker", tags=["Generic"])
def healthchecker():
    return {"message": "Welcome to Interactive Maps API"}
