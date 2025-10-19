from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import Base, engine
from routers import chat, auth, voice  # include voice router
from starlette.middleware import Middleware
# Create all tables (dev only)
Base.metadata.create_all(bind=engine)
origins = [
    "http://127.0.0.1:5500",  # your frontend URL
    "http://localhost:5500"
]

# app = FastAPI(title="EchoSense")
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],          # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],          # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],          # Allow all headers
# )

# -----------------------------
# Routers
# -----------------------------
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(voice.router, prefix="/api", tags=["Voice"])

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "EchoSense API is running!"}

# -----------------------------
# Global Exception Handler
# -----------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log error to console (useful for debugging)
    print(f"Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal Server Error: {str(exc)}"},
    )
