from fastapi import APIRouter, UploadFile, HTTPException, status
from src.files.service import save_and_upload_file

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile):
    try:
        file_url = await save_and_upload_file(file)
    except Exception as e:
        logger.exception(f"Error uploading file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
    return {"detail": f"Successfully uploaded {file.filename}", "file_url": file_url}
