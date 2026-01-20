from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.user.auth import router as auth_router

from app.api.v1.user.auth import router as student_router
from app.api.v1.user.auth import router as teacher_router

# Optional: import lifespan if you need startup/shutdown events
# from contextlib import asynccontextmanager
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # startup code
#     yield
#     # shutdown code

app = FastAPI(
    title="Academic Progress Tracking API",
    description="Backend system for students to submit academic progress and teachers to review/grade",
    version="0.1.0",
    # lifespan=lifespan,  # uncomment if you add startup/shutdown logic
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware (very useful during development with frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in production (e.g. ["http://localhost:3000", "https://yourfrontend.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# All user-related endpoints are under /api/v1/...
app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["auth"]
)

# Uncomment and add these as you implement the corresponding routers
#app.include_router(
     #student_router,
     #prefix="/api/v1/students",
     #tags=["students"])

#app.include_router(
     #teacher_router,
     #prefix="/api/v1/teachers",
    #tags=["teachers"] )

# Optional: root endpoint for health check
@app.get("/", tags=["health"])
async def root():
    return {"message": "Academic Progress Tracking API is running"}