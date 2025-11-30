from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from services import csv_service

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        print(f"Received file: {file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"Saved file to: {file_path}")

        # Load CSV into service
        csv_info = csv_service.load_csv(file_path)
        print(f"Loaded CSV info: {csv_info}")
        
        return JSONResponse(content={
            "message": "File uploaded successfully",
            "filename": file.filename,
            "info": csv_info
        })
    except Exception as e:
        print(f"Error during upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/csv-info")
async def get_csv_info():
    """Get information about the currently loaded CSV"""
    try:
        info = csv_service.get_csv_info()
        if not info:
            raise HTTPException(status_code=404, detail="No CSV file loaded")
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/csv-preview")
async def get_csv_preview(rows: int = 10):
    """Get a preview of the CSV data"""
    try:
        preview = csv_service.get_preview(rows)
        if preview is None:
            raise HTTPException(status_code=404, detail="No CSV file loaded")
        return {"preview": preview}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
