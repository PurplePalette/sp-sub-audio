from depends import MAXIMUM_FILESIZE, dependsFile, dependsFileSize
from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from task import AudioConversionTask

app = FastAPI()


@app.get("/")
async def get_root() -> JSONResponse:
    return JSONResponse(content={"message": "Server is running."})


@app.post("/convert")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = dependsFile,
    file_size: int = dependsFileSize,
) -> JSONResponse:
    file_type = file.content_type
    if file_type != "audio/mp3":
        raise HTTPException(status_code=400, detail="Invalid file type")
    if file_size > MAXIMUM_FILESIZE:
        raise HTTPException(status_code=400, detail="File size is too large")
    background_tasks.add_task(AudioConversionTask(file))
    return JSONResponse(content={"message": "started preview generating..."})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
