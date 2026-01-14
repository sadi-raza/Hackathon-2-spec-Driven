from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from .config import settings
from .database import lifespan
from .api.tasks import router as tasks_router
from .api.auth import router as auth_router


# Create FastAPI app with lifespan context
app = FastAPI(
    title="FastAPI Todo API Backend",
    description="Secure task management API for authenticated users",
    version="1.0.0",
    lifespan=lifespan,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])


# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc.errors()[0]["msg"]),
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_codes = {
        404: "NOT_FOUND",
        401: "UNAUTHORIZED",
        409: "CONFLICT",
    }
    code = error_codes.get(exc.status_code, "INTERNAL_ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": code, "message": exc.detail}},
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc.errors()[0]["msg"]),
            }
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI Todo API"}


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Todo API Backend"}