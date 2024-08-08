from fastapi import FastAPI
from config.routes import router_function
from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include router
# app.include_router(router_function, prefix="/api/v1")
app.include_router(router_function)
