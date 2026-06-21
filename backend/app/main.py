# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings

# Import routers trực tiếp
from app.routers.auth import router as auth_router
from app.routers.flights import router as flights_router
from app.routers.bookings import router as bookings_router
from app.routers.users import router as users_router
from app.routers.promotions import router as promotions_router
from app.routers.payments import router as payments_router
from app.routers.admin import router as admin_router

# Tạo tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Flight Ticket Booking API",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(flights_router)
app.include_router(bookings_router)
app.include_router(users_router)
app.include_router(promotions_router)
app.include_router(payments_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    return {
        "message": "Airline Booking API is running",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )