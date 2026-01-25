from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.user.auth import router as auth_router
from app.api.v1.enterprise.project import router as enterprise_projects_router

app = FastAPI(
    title="Academic Progress Tracking API",
    description="Backend system for students to submit academic progress and teachers to review/grade",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------

# Authentication & user-related endpoints
app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["auth"],
)

# Social Enterprise Project endpoints
app.include_router(
    enterprise_projects_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------
@app.get("/", tags=["health"])
async def root():
    return {"message": "Academic Progress Tracking API is running"}
