from pathlib import Path
import zipfile
import re
import uuid
import shutil
from utils import logger

class FileCreator:
    def __init__(self, root: Path, max_size: int = 2 * 1024 * 1024 * 1024):
        self.root = Path(root)
        self.max_size = max_size
        self.request_id = uuid.uuid4().hex
        self.request_folder = self.root / "requests" / self.request_id
        self.archives_folder = self.root / "archives"

        self.request_folder.mkdir(parents=True, exist_ok=True)
        self.archives_folder.mkdir(parents=True, exist_ok=True)

        logger.log("INFO", f"[{self.request_id}] Made working directory: {self.request_folder}")

    @staticmethod
    def sanitize_filename(name: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "_", name).strip() or "file"

    def add_file(self, title: str, text: str) -> Path:
        safe_name = self.sanitize_filename(title)
        file_path = self.request_folder / (safe_name + ".txt")

        i = 1
        while file_path.exists():
            file_path = self.request_folder / f"{safe_name}_{i}.txt"
            i += 1

        file_path.write_text(text, encoding="utf-8")
        logger.log("DEBUG", f"[{self.request_id}] File made: {file_path}")
        return file_path

    def create_archives(self) -> list[Path]:
        files = [p for p in sorted(self.request_folder.iterdir()) if p.is_file()]
        if not files:
            logger.log("WARN", f"[{self.request_id}] Haven't found any files in {self.request_folder}")
            return []

        output_paths: list[Path] = []
        part_index = 1
        current_size = 0
        current_zip = None

        def new_zip():
            nonlocal part_index, current_zip
            zip_path = self.archives_folder / f"archive_{self.request_id}_part{part_index}.zip"
            part_index += 1
            current_zip = zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED)
            output_paths.append(zip_path)
            logger.log("INFO", f"[{self.request_id}] Archive made: {zip_path}")
            return current_zip

        current_zip = new_zip()

        for f in files:
            fsize = f.stat().st_size
            if current_size + fsize > self.max_size and current_size > 0:
                current_zip.close()
                current_zip = new_zip()
                current_size = 0

            current_zip.write(f, arcname=f.name)
            logger.log("DEBUG", f"[{self.request_id}] Added file to archive: {f.name}")
            current_size += fsize

        current_zip.close()
        logger.log("INFO", f"[{self.request_id}] Archivation end")
        return output_paths

    def cleanup(self):
        if self.request_folder.exists():
            shutil.rmtree(self.request_folder, ignore_errors=True)
            logger.log("INFO", f"[{self.request_id}] Work directory cleanup")
