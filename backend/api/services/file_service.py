"""
File Upload Service
Handles resume upload, validation, and storage
"""
import os
import aiofiles
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

class FileService:
    """Service for handling file uploads and storage"""

    UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.pdf', '.PDF'}

    def __init__(self):
        # Create upload directory if it doesn't exist
        self.UPLOAD_DIR.mkdir(exist_ok=True)

    async def save_upload(self, file: UploadFile, student_id: int) -> tuple[str, str]:
        """
        Save uploaded file to disk

        Args:
            file: The uploaded file
            student_id: ID of the student profile

        Returns:
            Tuple of (file_path, filename)
        """
        # Validate file
        await self.validate_file(file)

        # Create unique filename
        file_extension = Path(file.filename).suffix
        safe_filename = f"resume_{student_id}_{file.filename.replace(' ', '_')}"
        file_path = self.UPLOAD_DIR / safe_filename

        # Save file asynchronously
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)

            logger.info(f"Saved file: {file_path}")
            return str(file_path), safe_filename

        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    async def validate_file(self, file: UploadFile) -> bool:
        """
        Validate uploaded file

        Args:
            file: The uploaded file

        Returns:
            True if valid

        Raises:
            HTTPException if invalid
        """
        # Check if file exists
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check file extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in {'.pdf'}:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Only PDF files are allowed. Got: {file_extension}"
            )

        # Check file size
        file.file.seek(0, 2)  # Move to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {self.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        return True

    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from disk

        Args:
            file_path: Path to the file

        Returns:
            True if deleted successfully
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False

    def get_file_path(self, filename: str) -> Optional[str]:
        """
        Get full path for a filename

        Args:
            filename: Name of the file

        Returns:
            Full path if file exists, None otherwise
        """
        file_path = self.UPLOAD_DIR / filename
        if file_path.exists():
            return str(file_path)
        return None

# Singleton instance
file_service = FileService()