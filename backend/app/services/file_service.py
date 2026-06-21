#backend/app/services/file_service.py
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from app.config import settings

class FileService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_file(self, file: UploadFile, folder: str = "images") -> Optional[str]:
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.pdf'}
        ext = Path(file.filename).suffix.lower()
        
        if ext not in allowed_extensions:
            return None
        
        # Tạo tên file unique
        filename = f"{uuid.uuid4()}{ext}"
        file_path = self.upload_dir / folder / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Lưu file
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return f"/uploads/{folder}/{filename}"
    
    def delete_file(self, file_path: str) -> bool:
        try:
            full_path = self.upload_dir / file_path.replace("/uploads/", "")
            if full_path.exists():
                full_path.unlink()
                return True
        except Exception:
            pass
        return False