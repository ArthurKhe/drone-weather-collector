from fastapi import FastAPI
from app.database import database, init_db
from app.routes import router

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    init_db()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router)
