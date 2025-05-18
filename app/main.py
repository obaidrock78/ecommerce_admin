import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from app.inventory import routes as inventory_routes
from app.middleware.exception_handlers import (
    error_handling_middleware,
    validation_exception_handler,
    handle_http_exception,
)
from config.config import settings

app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.PROJECT_VERSION,
    description="This is a description of my API",
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Register the exception handlers
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

# Register the error handling middleware
app.middleware("http")(error_handling_middleware)

os.makedirs("media", exist_ok=True)
os.makedirs("static", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")


@app.get("/health_check", tags=["Service Health Check"])
def health_check():
    return {
        "status": "active",
        "service_name": settings.SERVICE_NAME,
        "environment": settings.PROJECT_VERSION,
    }


app.include_router(inventory_routes.router, prefix="/inventory", tags=["inventory"])


# Redirect the root path to Swagger docs
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def redirect_to_swagger():
    return RedirectResponse(url=f"{settings.BASE_URL}/user-service/user-docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
