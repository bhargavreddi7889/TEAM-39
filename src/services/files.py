import os
import uuid
from pathlib import Path
from datetime import datetime
from src.config import get_settings

# Data directory for storing uploaded files
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


class FileService:
    """Service for managing uploaded files."""
    
    def __init__(self):
        # Ensure data directory exists
        DATA_DIR.mkdir(exist_ok=True)
    
    def list_files(self) -> list[dict]:
        """List all uploaded files with metadata."""
        files = []
        for filepath in DATA_DIR.iterdir():
            if filepath.is_file() and filepath.name != ".gitkeep":
                stat = filepath.stat()
                files.append({
                    "filename": filepath.name,
                    "size_bytes": stat.st_size,
                    "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        # Sort by upload time (newest first)
        files.sort(key=lambda x: x["uploaded_at"], reverse=True)
        return files
    
    def save_file(self, filename: str, content: bytes) -> dict:
        """Save uploaded file to data directory."""
        # Sanitize filename and make unique if exists
        safe_name = self._sanitize_filename(filename)
        filepath = DATA_DIR / safe_name
        
        # If file exists, add timestamp to make unique
        if filepath.exists():
            name, ext = os.path.splitext(safe_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = f"{name}_{timestamp}{ext}"
            filepath = DATA_DIR / safe_name
        
        # Write file
        filepath.write_bytes(content)
        
        return {
            "filename": safe_name,
            "size_bytes": len(content),
            "path": str(filepath)
        }
    
    def get_file(self, filename: str) -> tuple[bytes, str] | None:
        """Get file content and path. Returns None if not found."""
        filepath = DATA_DIR / filename
        if filepath.exists() and filepath.is_file():
            return filepath.read_bytes(), str(filepath)
        return None
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file. Returns True if deleted, False if not found."""
        filepath = DATA_DIR / filename
        if filepath.exists() and filepath.is_file():
            filepath.unlink()
            return True
        return False
    
    def file_exists(self, filename: str) -> bool:
        """Check if a file exists."""
        filepath = DATA_DIR / filename
        return filepath.exists() and filepath.is_file()
    
    def get_file_path(self, filename: str) -> Path | None:
        """Get the full path to a file."""
        filepath = DATA_DIR / filename
        if filepath.exists():
            return filepath
        return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent directory traversal attacks."""
        # Remove any path components, keep only the filename
        return os.path.basename(filename).replace(" ", "_")

