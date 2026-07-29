from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routers import appointments, auth

app = FastAPI(
    title="QueueCare",
    description="Clinic appointment and queue management API",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(appointments.router)


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    """Return 400 for malformed input instead of FastAPI's default 422."""
    first = exc.errors()[0]
    field = ".".join(str(part) for part in first["loc"] if part != "body")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"{field}: {first['msg']}"},
    )


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "QueueCare"}


@app.get("/", include_in_schema=False)
def index():
    return FileResponse("app/static/login.html")


app.mount("/static", StaticFiles(directory="app/static"), name="static")