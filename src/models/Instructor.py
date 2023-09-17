import uuid
from typing import Dict

class Instructor:
    def __init__(self, name: str) -> None:
        self.name: str = name
        generated_uuid = str(uuid.uuid4())
        # check if uuid is unique
        self.id: str = generated_uuid
        self.saved_files: Dict[str, str] = {}

    def add_file(self, file_type: str, file_name: str) -> None:
        if file_type not in ['readings', 'curricula', 'lectures']:
            raise ValueError('Invalid file type')
        self.saved_files[file_type] = file_name
