from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, brain_dumps, tasks, shopping_items, calendar_events
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup: Initialize database tables
    try:
        init_db()
        print("✓ Database connected and initialized")
    except Exception as e:
        print(f"⚠ Warning: Could not connect to database: {e}")
        print("  Server will start but database operations will fail.")
        print("  Please check your DATABASE_URL and ensure Supabase is unpaused.")

    yield
    # Shutdown: Add cleanup code here if needed


# Initialize FastAPI app
app = FastAPI(
    title="Diane Backend",
    description="Mental load management for parents",
    version="1.0.0",
    lifespan=lifespan,
)


# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(brain_dumps.router)
app.include_router(tasks.router)
app.include_router(shopping_items.router)
app.include_router(calendar_events.router)


@app.get("/")
def read_root():
    return {"message": "Diane Backend API", "status": "running", "version": "1.0.0"}
