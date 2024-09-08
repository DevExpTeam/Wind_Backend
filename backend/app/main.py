from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import engine, metadata, database
from app.api.routes import auth, user, parameter, calculator
metadata.create_all(engine)

app = FastAPI() 
origins = [
    "http://localhost", 
    "*"
] 
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["DELETE", "GET", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# app.include_router(input.router, prefix="/input", tags=["input"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(parameter.router, prefix="/parameter", tags=["parameter"])
app.include_router(calculator.router, prefix="/calculator", tags=["calculator"])
# app.include_router(historyData.router, prefix="/historyData", tags=["historyData"])

