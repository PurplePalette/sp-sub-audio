from fastapi import Depends, File, Header
from config import MAXIMUM_FILESIZE


dependsMaximumFileSize = Header(..., lt=MAXIMUM_FILESIZE)


async def valid_content_length(content_length: int = dependsMaximumFileSize) -> int:
    return content_length


dependsFile = File(None, description="")
dependsFileSize = Depends(valid_content_length)
