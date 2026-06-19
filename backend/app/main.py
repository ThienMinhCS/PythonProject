# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth_router, flights_router, bookings_router, users_router
from app.config import settings

# Tạo tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Flight Ticket Booking API",
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# 👉 SỬA CORS - CHO PHÉP FRONTEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite frontend
        "http://localhost:3000",   # React default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # Cho phép tất cả (chỉ dùng khi dev)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(flights_router)
app.include_router(bookings_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {
        "message": "Airline Booking API is running",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )