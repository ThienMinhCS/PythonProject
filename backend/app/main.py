from fastapi import FastAPI

app = FastAPI(
    title="Airline Booking System",
    description="Flight Ticket Booking API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Airline Booking API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }