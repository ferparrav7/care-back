import os
import random
import string
import aiofiles
import tempfile
import logging

from src.files.b2 import b2_upload_file

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024

def get_temp_filename():
    tmp_dir = tempfile.gettempdir()
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return os.path.join(tmp_dir, random_name)

async def save_and_upload_file(file):
    filename = get_temp_filename()
    logger.info(f"Saving uploaded file temporarily to {filename}")
    async with aiofiles.open(filename, "wb") as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)
    file_url = b2_upload_file(local_file=filename, file_name=file.filename)
    os.remove(filename)
    return file_url