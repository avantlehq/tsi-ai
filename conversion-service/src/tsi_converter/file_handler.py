"""
File upload and download handling for TSI conversion service.
"""

import os
import json
import tempfile
import uuid
from typing import Dict, Any, Optional, BinaryIO
from pathlib import Path
from fastapi import UploadFile, HTTPException


class FileHandler:
    """Handles file operations for the conversion service."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize file handler.
        
        Args:
            storage_path: Path for temporary file storage
        """
        self.storage_path = storage_path or tempfile.gettempdir()
        self.storage_dir = Path(self.storage_path) / "tsi_converter"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile, job_id: str) -> str:
        """
        Save uploaded file to temporary storage.
        
        Args:
            file: Uploaded file
            job_id: Job identifier for file organization
            
        Returns:
            Path to saved file
            
        Raises:
            HTTPException: If file operations fail
        """
        try:
            # Create job directory
            job_dir = self.storage_dir / job_id
            job_dir.mkdir(exist_ok=True)
            
            # Generate safe filename
            safe_filename = self._sanitize_filename(file.filename or "upload.json")
            file_path = job_dir / safe_filename
            
            # Save file
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            return str(file_path)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save uploaded file: {str(e)}"
            )
    
    async def read_json_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read and parse JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
            
        Raises:
            HTTPException: If file reading or parsing fails
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return json.loads(content)
                
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON file: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read file: {str(e)}"
            )
    
    async def save_output_file(self, job_id: str, filename: str, content: str) -> str:
        """
        Save conversion output to file.
        
        Args:
            job_id: Job identifier
            filename: Output filename
            content: File content
            
        Returns:
            Path to saved file
        """
        try:
            job_dir = self.storage_dir / job_id
            job_dir.mkdir(exist_ok=True)
            
            file_path = job_dir / filename
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return str(file_path)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save output file: {str(e)}"
            )
    
    async def save_binary_file(self, job_id: str, filename: str, content: bytes) -> str:
        """
        Save binary content to file.
        
        Args:
            job_id: Job identifier
            filename: Output filename
            content: Binary content
            
        Returns:
            Path to saved file
        """
        try:
            job_dir = self.storage_dir / job_id
            job_dir.mkdir(exist_ok=True)
            
            file_path = job_dir / filename
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            return str(file_path)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save binary file: {str(e)}"
            )
    
    def get_file_path(self, job_id: str, filename: str) -> str:
        """
        Get full path to file in job directory.
        
        Args:
            job_id: Job identifier
            filename: Filename
            
        Returns:
            Full file path
        """
        return str(self.storage_dir / job_id / filename)
    
    def file_exists(self, job_id: str, filename: str) -> bool:
        """
        Check if file exists in job directory.
        
        Args:
            job_id: Job identifier
            filename: Filename
            
        Returns:
            True if file exists
        """
        file_path = Path(self.storage_dir) / job_id / filename
        return file_path.exists()
    
    async def cleanup_job_files(self, job_id: str) -> None:
        """
        Remove all files for a job.
        
        Args:
            job_id: Job identifier
        """
        try:
            job_dir = self.storage_dir / job_id
            if job_dir.exists():
                import shutil
                shutil.rmtree(job_dir)
                
        except Exception:
            # Ignore cleanup errors
            pass
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for safe filesystem operations.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path separators and dangerous characters
        import re
        safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
        
        # Limit length
        if len(safe_filename) > 100:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = name[:95] + ext
        
        # Ensure we have an extension
        if '.' not in safe_filename:
            safe_filename += '.txt'
        
        return safe_filename


# Global file handler instance
file_handler = FileHandler()