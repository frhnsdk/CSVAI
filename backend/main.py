from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routes import csv_routes, chat_routes

app = FastAPI(title="CSV AI", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(csv_routes.router, prefix="/api", tags=["CSV"])
app.include_router(chat_routes.router, prefix="/api", tags=["Chat"])

# Serve frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
# Serve photos (logo) from root photos/ so frontend can reference /photos/logo.svg
photos_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "photos")
if os.path.exists(photos_path):
    app.mount("/photos", StaticFiles(directory=photos_path), name="photos")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
