from fastapi import FastAPI
from app import routes
from app.database import database, init_db

app = FastAPI()


# Initialize the database
@app.on_event("startup")
async def startup():
    await database.connect()
    init_db()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Include the authentication routes
app.include_router(routes.router)
